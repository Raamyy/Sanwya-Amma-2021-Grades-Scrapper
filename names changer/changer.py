from faker import Faker
from faker.providers.person.ar_AA import Provider


fake = Faker('ar_AA')
fake.add_provider(Provider)

school_hash = {}
school_index = 1
    
def generate_name():
    return fake.name().strip()


i = 1
with open('students_data_annoynmous_names.csv', 'w', encoding="utf8") as result:
    with open('students_data.csv', 'r', encoding="utf8") as f:
        while True:
            students_data = f.readline()
            if not students_data:
                break
            cols =  students_data.split(',')
            if i > 1:
                cols[4] = generate_name()
                school_name = cols[5]
                if school_name not in school_hash:
                    school_hash[school_name] = school_index
                cols[5] = str(school_hash[school_name])
                school_index += 1
            result.write(','.join(cols))
            i += 1

    