//
// Created by Glavak on 9/27/2016.
//

#include <stdio.h>

#include "vm.h"

void vm_print(unsigned char * str)
{
    printf("%s", str);
}

int vm_read()
{
    int res;
    printf(">");
    scanf("%d", &res);
    return res;
}

void main()
{
    struct vm_settings settings;

    settings.program_filename = (unsigned char *) "../program";
    settings.print = &vm_print;
    settings.read = &vm_read;

    start_vm(settings);
}
