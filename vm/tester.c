//
// Created by Glavak on 9/27/2016.
//

#include <stdio.h>
#include <stdlib.h>

#include "vm.h"

char *expected_output;
int symbols_printed;
int failed;

void vm_print(char *str)
{
    while (*str != '\0')
    {
        if (*str != *expected_output)
        {
            failed = 1;
        }

        if (expected_output == '\0')
        {
            // Program writes too much
            failed = 1;
        }
        else
        {
            expected_output++;
            symbols_printed++;
            str++;
        }
    }
}

void get_expected_output(char *filename)
{
    FILE *file;
    fopen_s(&file, filename, "r");

    // FIXME: reads only one line
    expected_output = malloc(sizeof(byte) * 1024);
    fscanf(file, "%s", expected_output);

    fclose(file);
}

void launch_test(int number)
{
    char f[100];
    sprintf(f, "tests/%d.out", number);

    get_expected_output(f);
    symbols_printed = 0;
    failed = 0;

    struct vm_settings settings;

    sprintf(f, "tests/%d", number);
    settings.program_filename = f;
    settings.print = &vm_print;

    start_vm(settings);

    if (*expected_output != '\0')
    {
        // Program wrote less than required
        failed = 1;
    }

    if (failed)
    {
        printf("Test %d failed!\n", number);
    }
    else
    {
        printf("Test %d passed!\n", number);
    }
}

void main()
{
    launch_test(1);
    launch_test(2);
}
