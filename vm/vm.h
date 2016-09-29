//
// Created by Glavak on 9/27/2016.
//

#ifndef VM_VM_H
#define VM_VM_H

typedef unsigned char byte;

struct vm_settings
{
    char * program_filename;

    // Function, which will be called by vm when it want to print something to console
    void (*print)(char *);

    // Function, which will be called by vm when it want to read something from console
    int (*read)();
};

int start_vm(struct vm_settings settings);

#endif //VM_VM_H
