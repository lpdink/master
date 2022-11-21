#include <iostream>
#include <string>
using namespace std;
class Student
{
public:
    // friend void show_info(const Student* ptr);
    friend class Teacher;
    Student(const string name, const unsigned int age, const unsigned int number, float score) : name(name), age(age), number(number), score(score) {}

private:
    const std::string name;
    const unsigned int age;
    const unsigned int number;
    float score;
};

class Teacher
{
public:
    void show_info(const Student *ptr)
    {
        std::cout << __func__ << "\n name:" << ptr->name << " age:" << ptr->age << " number:" << ptr->number << std::endl;
    }
};

int main()
{
    Student student = Student("Tom", 14, 114514, 88.42);
    Teacher teacher = Teacher();
    teacher.show_info(&student);
}