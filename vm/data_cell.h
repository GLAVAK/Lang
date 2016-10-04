//
// Created by Glavak on 10/3/2016.
//

#ifndef VM_DATA_CELL_H
#define VM_DATA_CELL_H

struct data_cell
{
    union
    {
        double f;
        int i;
        int b;
        char * s;
    } data;
};

#endif //VM_DATA_CELL_H
