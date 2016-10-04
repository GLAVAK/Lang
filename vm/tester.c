//
// Created by Glavak on 9/27/2016.
//

#include <stdio.h>

#include "vm.h"
#include "utils.h"

unsigned char * expected_output;
int symbols_printed;
int failed;

void vm_print(unsigned char * str)
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

void launch_test(int number)
{
    char f[100];
    sprintf(f, "tests/%d.out", number);

    size_t expected_output_size;
    expected_output = read_file(f, &expected_output_size);
    symbols_printed = 0;
    failed = 0;

    struct vm_settings settings;

    sprintf(f, "tests/%d", number);
    settings.program_filename = (unsigned char *) f;
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
    // TODO: rework tester, make it compile code and test it, not the bytecode
    int tests_count = 0;

    for (int i = 1; i <= tests_count; ++i)
    {
        launch_test(i);
    }
}
