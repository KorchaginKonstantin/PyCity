from random import randint


with open('map.txt') as file_count:
    for line in file_count:
        num = len(line.strip())


def generate_hor(per):
    file_list = []

    with open('map.txt', 'r+') as file:
        for line in file:
            line_list = []

            for char in line:
                if char == '1':
                    char = '0'
                if char != '\n':
                    line_list.append(char)

            file_list.append(line_list)

        num_seek_hor = randint(per, len(file_list) - 1) * (len(file_list[0]) + 1)

        for i in range(per):
            file.seek(num_seek_hor - (len(file_list[0])*i + i))
            file.write(''.join(file_list[0]))


def generate_ver():
    with open('map.txt', 'r+') as file:
        file_list = []
        num_seek_ver = randint(1, num - 1)

        for line in file:
            count = 0
            line_list = []

            for char in line:
                if count == num_seek_ver or count == num_seek_ver - 1:
                    line_list.append('0')
                elif char != '\n':
                    line_list.append(char)

                count += 1

            file_list.append(line_list)

        for count_for in range(len(file_list)):
            file.seek((len(file_list[0]) + 1) * count_for)
            file.write(''.join(file_list[count_for]))