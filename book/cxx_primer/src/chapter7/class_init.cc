#include <iostream>
#include <string>
class Student
{
public:
    Student(const std::string name, const unsigned int age, const unsigned int id, float score) : name(name), age(age), number(id), score(score) {}
    friend void show_info(const Student *ptr);
    void show_info()
    {
        std::cout << __func__ << "\nname:" << this->name << " age:" << this->age << " number:" << this->number << std::endl;
    }

private:
    const std::string name;
    const unsigned int age;
    const unsigned int number;
    float score;
};

void show_info(const Student *ptr)
{
    std::cout << __func__ << "\nname:" << ptr->name << " age:" << ptr->age << " number:" << ptr->number << std::endl;
}

int main()
{
    Student student = Student("小布丁", 22, 114514, 66.42);
    student.show_info();
    auto *ptr = &student;
    show_info(ptr);
    
}