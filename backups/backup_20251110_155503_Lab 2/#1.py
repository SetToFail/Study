import os
import logging
import shutil
from pathlib import Path
from datetime import datetime
import time
from tqdm import tqdm

class RLEArchiverWithLogging:
    def __init__(self, log_file="archiver.log"):
        """Инициализация архиватора с логированием"""
        self.setup_logging(log_file)
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def setup_logging(self, log_file):
        """Настройка системы логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # Вывод также в консоль
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("=== RLE Archiver запущен ===")
    
    def create_backup(self, folder_path):
        """Создание резервной копии перед операцией"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}_{Path(folder_path).name}"
        backup_path = self.backup_dir / backup_name
        
        try:
            self.logger.info(f"Создание резервной копии: {folder_path} -> {backup_path}")
            if Path(folder_path).is_dir():
                shutil.copytree(folder_path, backup_path)
            else:
                shutil.copy2(folder_path, backup_path)
            self.logger.info(f"Резервная копия создана: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Ошибка создания резервной копии: {e}")
            return None
    
    def rollback(self, backup_path, target_path):
        """Откат изменений из резервной копии"""
        try:
            self.logger.info(f"Начало отката: {backup_path} -> {target_path}")
            
            # Удаляем целевой путь если существует
            if Path(target_path).exists():
                if Path(target_path).is_dir():
                    shutil.rmtree(target_path)
                else:
                    os.remove(target_path)
            
            if Path(backup_path).is_dir():
                shutil.copytree(backup_path, target_path)
            else:
                shutil.copy2(backup_path, target_path)
            
            self.logger.info(f"Откат завершен успешно: {target_path}")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка отката: {e}")
            return False
    
    def rle_compress(self, data):
        """Простое RLE сжатие"""
        result = bytearray()
        i = 0
        while i < len(data):
            count = 1
            while i + count < len(data) and data[i] == data[i + count] and count < 255:
                count += 1
            result.extend([count, data[i]])
            i += count
        return bytes(result)
    
    def rle_decompress(self, data):
        """Простое RLE распаковка"""
        result = bytearray()
        for i in range(0, len(data), 2):
            count, byte = data[i], data[i+1]
            result.extend([byte] * count)
        return bytes(result)
    
    def compress_folder(self, folder_path, output_file):
        """Сжать папку с логированием и прогресс-баром"""
        self.logger.info(f"НАЧАЛО СЖАТИЯ: {folder_path} -> {output_file}")
        start_time = time.time()
        
        try:
            backup_path = self.create_backup(folder_path)
            
            with open(output_file, 'wb') as archive:
                archive.write(b'RLE')
                
                all_files = list(Path(folder_path).rglob('*'))
                file_list = [f for f in all_files if f.is_file()]
                
                self.logger.info(f"Найдено файлов для сжатия: {len(file_list)}")
                
                with tqdm(total=len(file_list), desc=" Сжатие файлов", unit="file") as pbar:
                    for file_path in file_list:
                        try:
                            rel_path = str(file_path.relative_to(folder_path))
                            self.logger.debug(f"Сжимаем файл: {rel_path}")
                            
                            with open(file_path, 'rb') as f:
                                original = f.read()
                            
                            compressed = self.rle_compress(original)
                            
                            archive.write(rel_path.encode() + b'\n')
                            archive.write(compressed)
                            archive.write(b'\x00')
                            
                            pbar.set_postfix(file=rel_path[-20:])  # Показываем окончание имени файла
                            pbar.update(1)
                            
                        except Exception as e:
                            self.logger.error(f"Ошибка сжатия файла {file_path}: {e}")
                            continue
                
                original_size = sum(f.stat().st_size for f in file_list)
                compressed_size = os.path.getsize(output_file)
                compression_ratio = (1 - compressed_size / original_size) * 100
                elapsed_time = time.time() - start_time
                
                self.logger.info(f"СЖАТИЕ ЗАВЕРШЕНО: {output_file}")
                self.logger.info(f"Статистика: {original_size} -> {compressed_size} байт")
                self.logger.info(f"Сжатие: {compression_ratio:.1f}%")
                self.logger.info(f"Время выполнения: {elapsed_time:.2f} сек")
                
                print(f" Готово! Архив: {output_file}")
                print(f" Сжатие: {compression_ratio:.1f}%")
                print(f" Время: {elapsed_time:.2f} сек")
                
                return True
                
        except Exception as e:
            self.logger.error(f"КРИТИЧЕСКАЯ ОШИБКА ПРИ СЖАТИИ: {e}")
            print(f"❌ Ошибка при сжатии: {e}")
            return False
    
    def decompress_folder(self, archive_file, output_folder):
        """Распаковать архив с логированием и прогресс-баром"""
        self.logger.info(f"НАЧАЛО РАСПАКОВКИ: {archive_file} -> {output_folder}")
        start_time = time.time()
        
        try:
            backup_path = self.create_backup(archive_file)
            
            with open(archive_file, 'rb') as archive:
                if archive.read(3) != b'RLE':
                    error_msg = "Это не RLE архив!"
                    self.logger.error(error_msg)
                    print(f" {error_msg}")
                    return False
                
                Path(output_folder).mkdir(exist_ok=True)
                
                self.logger.info("Подсчет файлов в архиве...")
                archive.seek(3)  
                file_count = 0
                
                temp_archive = open(archive_file, 'rb')
                temp_archive.read(3)
                while True:
                    name = b''
                    while True:
                        byte = temp_archive.read(1)
                        if byte == b'\n' or not byte:
                            break
                        name += byte
                    if not name:
                        break
                    while True:
                        byte = temp_archive.read(1)
                        if byte == b'\x00' or not byte:
                            break
                    file_count += 1
                temp_archive.close()
                
                self.logger.info(f"Файлов в архиве: {file_count}")
                
                archive.seek(3)
                
                with tqdm(total=file_count, desc=" Распаковка файлов", unit="file") as pbar:
                    files_processed = 0
                    
                    while files_processed < file_count:
                        name = b''
                        while True:
                            byte = archive.read(1)
                            if byte == b'\n' or not byte:
                                break
                            name += byte
                        
                        if not name:
                            break
                        
                        compressed = b''
                        while True:
                            byte = archive.read(1)
                            if byte == b'\x00' or not byte:
                                break
                            compressed += byte
                        
                        try:
                            original = self.rle_decompress(compressed)
                            file_path = Path(output_folder) / name.decode()
                            file_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            with open(file_path, 'wb') as f:
                                f.write(original)
                            
                            self.logger.debug(f"Распакован файл: {name.decode()}")
                            pbar.set_postfix(file=name.decode()[-20:])
                            pbar.update(1)
                            files_processed += 1
                            
                        except Exception as e:
                            self.logger.error(f"Ошибка распаковки файла {name}: {e}")
                            continue
                
                elapsed_time = time.time() - start_time
                self.logger.info(f"РАСПАКОВКА ЗАВЕРШЕНА: {output_folder}")
                self.logger.info(f"Распаковано файлов: {files_processed}")
                self.logger.info(f"Время выполнения: {elapsed_time:.2f} сек")
                
                print(f" Распаковка завершена! Файлов: {files_processed}")
                print(f" Время: {elapsed_time:.2f} сек")
                
                return True
                
        except Exception as e:
            self.logger.error(f"КРИТИЧЕСКАЯ ОШИБКА ПРИ РАСПАКОВКЕ: {e}")
            print(f" Ошибка при распаковке: {e}")
            
            if backup_path and Path(backup_path).exists():
                choice = input("Произошла ошибка. Выполнить откат? (y/n): ")
                if choice.lower() == 'y':
                    self.rollback(backup_path, archive_file)
            return False
    
    def show_backups(self):
        """Показать доступные резервные копии"""
        backups = list(self.backup_dir.glob("backup_*"))
        if not backups:
            print("Резервные копии не найдены")
            return
        
        print("\n Доступные резервные копии:")
        for i, backup in enumerate(sorted(backups), 1):
            size = backup.stat().st_size if backup.is_file() else sum(
                f.stat().st_size for f in backup.rglob('*') if f.is_file()
            )
            print(f"{i}. {backup.name} ({size / 1024:.1f} KB)")
        
        return backups

# ИНТЕРАКТИВНЫЙ РЕЖИМ
def main():
    archiver = RLEArchiverWithLogging()
    
    while True:
        print("\n" + "="*50)
        print(" RLE АРХИВАТОР С ЛОГИРОВАНИЕМ")
        print("="*50)
        print("1. Сжать папку")
        print("2. Распаковать архив")
        print("3. Показать резервные копии")
        print("4. Выполнить откат")
        print("5. Показать логи")
        print("6. Выход")
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == '1':
            folder = input("Путь к папке для сжатия: ").strip()
            output = input("Куда сохранить архив: ").strip()
            archiver.compress_folder(folder, output)
            
        elif choice == '2':
            archive = input("Путь к архиву: ").strip()
            output = input("Куда распаковать: ").strip()
            archiver.decompress_folder(archive, output)
            
        elif choice == '3':
            archiver.show_backups()
            
        elif choice == '4':
            backups = archiver.show_backups()
            if backups:
                try:
                    backup_num = int(input("Номер резервной копии для отката: ")) - 1
                    if 0 <= backup_num < len(backups):
                        target = input("Куда восстановить: ").strip()
                        archiver.rollback(backups[backup_num], target)
                    else:
                        print("Неверный номер")
                except ValueError:
                    print("Введите число")
            
        elif choice == '5':
            # Показать последние 10 строк лога
            if os.path.exists("archiver.log"):
                with open("archiver.log", "r", encoding='utf-8') as f:
                    lines = f.readlines()
                    print("\n".join(lines[-10:]))
            else:
                print("Файл логов не найден")
            
        elif choice == '6':
            archiver.logger.info("=== RLE Archiver остановлен ===")
            break
            
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()