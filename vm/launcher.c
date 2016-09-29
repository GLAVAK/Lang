//
// Created by Glavak on 9/27/2016.
//

#include <stdio.h>

#include "vm.h"

void vm_print(char * str)
{
    printf("%s", str);
}

void main()
{
    struct vm_settings settings;

    settings.program_filename = "prog";
    settings.print = &vm_print;

    start_vm(settings);
}
