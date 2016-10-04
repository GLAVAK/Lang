//
// Created by Glavak on 9/27/2016.
//

#include <stdio.h>
#include <malloc.h>

#include "vm.h"

void vm_print(unsigned char * str)
{
    printf("%s", str);
}

char * vm_read()
{
    char * s = malloc(sizeof(char) * 256);
    printf(">");
    scanf("%s", s);
    return s;
}

void main()
{
    struct vm_settings settings;

    settings.program_filename = (unsigned char *) "../program";
    settings.print = &vm_print;
    settings.read = &vm_read;

    start_vm(settings);
}
