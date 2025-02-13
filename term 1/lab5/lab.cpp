#include <iostream>
#include <vector>
#include <string>
#include <algorithm> 
class Book
{
protected: // protected для доступа в наследниках
    std::string _title;
    std::string _author;
    int _year;
    std::string _genre;

public:
    // Конструктор
    Book(const std::string &title, const std::string &author, int year, const std::string &genre)
        : _title(title), _author(author), _year(year), _genre(genre) {}
    // Геттеры для доступа к атрибутам
    std::string getTitle() const { return _title; }
    std::string getAuthor() const { return _author; }
    int getYear() const { return _year; }
    std::string getGenre() const { return _genre; }
    // Сеттеры для изменения атрибутов
    void setTitle(const std::string &title) { _title = title; }
    void setAuthor(const std::string &author) { _author = author; }
    void setYear(int year) { _year = year; }
    void setGenre(const std::string &genre) { _genre = genre; }
    // Метод для вывода информации (виртуальный для полиморфизма)
    virtual std::string displayInfo() const
    {
        return "Название: " + _title + ", Автор: " + _author + ", Год: " + std::to_string(_year) + ", Жанр: " + _genre;
    }
    virtual ~Book() = default; // Виртуальный деструктор для полиморфизма
};
class EBook : public Book
{
private:
    std::string _fileFormat;
    std::string _fileSize;
public:
    EBook(const std::string &title, const std::string &author, int year, const std::string &genre,
          const std::string &fileFormat, const std::string &fileSize)
        : Book(title, author, year, genre), _fileFormat(fileFormat), _fileSize(fileSize) {}
    // Геттеры
    std::string getFileFormat() const { return _fileFormat; }
    std::string getFileSize() const { return _fileSize; }
    // Сеттеры
    void setFileFormat(const std::string &fileFormat) { _fileFormat = fileFormat; }
    void setFileSize(const std::string &fileSize) { _fileSize = fileSize; }
    // Переопределенный метод displayInfo
    std::string displayInfo() const override
    {
        return "Название: " + _title + ", Автор: " + _author + ", Год: " + std::to_string(_year) + ", Жанр: " + _genre + ", Формат: " + _fileFormat + ", Размер: " + _fileSize;
    }
};
class ABook : public Book
{
private:
    std::string _fileFormat;
    std::string _fileSize;

public:
    ABook(const std::string &title, const std::string &author, int year, const std::string &genre,
          const std::string &fileFormat, const std::string &fileSize)
        : Book(title, author, year, genre), _fileFormat(fileFormat), _fileSize(fileSize) {}

    // Геттеры
    std::string getFileFormat() const { return _fileFormat; }
    std::string getFileSize() const { return _fileSize; }
    // Сеттеры
    void setFileFormat(const std::string &fileFormat) { _fileFormat = fileFormat; }
    void setFileSize(const std::string &fileSize) { _fileSize = fileSize; }
    // Переопределенный метод displayInfo
    std::string displayInfo() const override
    {
        return "Название: " + _title + ", Автор: " + _author + ", Год: " + std::to_string(_year) + ", Жанр: " + _genre + ", Формат: " + _fileFormat + ", Размер: " + _fileSize;
    }
};
class Library
{
private:
    std::vector<Book *> _books; // Вектор для хранения указателей на объекты Book (для полиморфизма)
public:
    // Деструктор для освобождения памяти
    ~Library()
    {
        for (Book *book : _books)
        {
            delete book; // Освобождаем память для каждой книги
        }
    }
    // Метод для добавления книги
    void addBook(Book *book)
    {
        _books.push_back(book);
    }
    // Метод для удаления книги
    void removeBook(const std::string &title)
    {
        for (size_t i = 0; i < _books.size(); ++i)
        {
            if (_books[i]->getTitle() == title)
            {
                delete _books[i]; // Освобождаем память
                _books.erase(_books.begin() + i);
                return;
            }
        }
    }
    // Метод для поиска книги
    Book *searchBook(const std::string &title)
    {
        for (Book *book : _books)
        {
            if (book->getTitle() == title)
            {
                return book;
            }
        }
        return nullptr; // Если книга не найдена
    }
    // Метод для вывода информации о всех книгах
    void displayAllBooks() const
    {
        for (Book *book : _books)
        {
            std::cout << book->displayInfo() << std::endl;
        }
    }
    std::vector<Book *> getAllBooks() const
    {
        return _books;
    }
};
int main()
{
    // Создаем книги разных типов
    Book *book1 = new Book("Мастер и Маргарита", "М. Булгаков", 1967, "Роман");
    Book *book2 = new EBook("Гарри Поттер и философский камень", "Дж. К. Роулинг", 1997, "Фэнтези", "pdf", "2.5MB");
    Book *book3 = new ABook("1984", "Дж. Оруэлл", 1949, "Антиутопия", "mp3", "50MB");
    Book *book4 = new Book("Преступление и наказание", "Ф. Достоевский", 1866, "Роман");
    // Создаем библиотеку и добавляем книги
    Library library;
    library.addBook(book1);
    library.addBook(book2);
    library.addBook(book3);
    library.addBook(book4);
    // Выводим информацию о всех книгах
    std::cout << "Все книги в библиотеке:" << std::endl;
    library.displayAllBooks();
    std::cout << std::endl;
    // Поиск книги
    std::string searchTitle = "Гарри Поттер и философский камень";
    Book *foundBook = library.searchBook(searchTitle);
    if (foundBook)
    {
        std::cout << "Книга '" << searchTitle << "' найдена: " << foundBook->displayInfo() << std::endl;
    }
    else
    {
        std::cout << "Книга '" << searchTitle << "' не найдена." << std::endl;
    }
    std::cout << std::endl;
    // Удаление книги
    library.removeBook("Мастер и Маргарита");
    std::cout << "Все книги после удаления одной из них:" << std::endl;
    library.displayAllBooks();
    std::cout << std::endl;
    // Выводим снова информацию обо всех книгах
    std::cout << "Все книги в библиотеке (после удаления):" << std::endl;
    for (Book *book : library.getAllBooks())
    {
        std::cout << book->displayInfo() << std::endl;
    }
    return 0;
}