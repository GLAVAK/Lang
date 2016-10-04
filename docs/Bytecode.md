# Programming language with no name yet, bytecode
## Stack and memory

Program executed in a stack based virtual machine. It has stack with maximum size of 128 data cells, and memory of 256 data cells. All operations performed on a stack.

## Operands data types

`integer` - big endian, 4 bytes
`float` - big endian, 8 bytes
`string` - not more than 255 ASCII characters, \0-terminated
`addr` - 1 byte

## Opcodes

| Alias      | Hex value | Operands/stack data types | Description
| ---------- | --------- | ------------------------- | ---
| Stack/memory operations: | | |
| PushValI   | 0x01      | 1 integer, ->i            |
| PushValF   | 0x02      | 1 float,   ->f            |
| PushValS   | 0x03      | 1 string,  ->s            |
| PopMem     | 0x15      | 1 addr,   x->             |
| SeekMem    | 0x16      | 1 addr,   x->x            | Same as PopMem, bot w/o actual popping
| Integer operations: | | |
| AddI       | 0x30      |         i,i->i            |
| SubI       | 0x31      |         i,i->i            |
| MulI       | 0x32      |         i,i->i            |
| DivI       | 0x33      |         i,i->i            |
| InvertI    | 0x34      |           i->i            |
| Integer comparison: | | |
| EqualsI    | 0x3A      |         i,i->b            |
| !EqualsI   | 0x3B      |         i,i->b            |
| GreaterI   | 0x3C      |         i,i->b            |
| LessI      | 0x3D      |         i,i->b            |
| GreaterEqI | 0x3E      |         i,i->b            |
| LessEqI    | 0x3F      |         i,i->b            |
| Float operations: | | |
| AddF       | 0x40      |         f,f->f            |
| SubF       | 0x41      |         f,f->f            |
| MulF       | 0x42      |         f,f->f            |
| DivF       | 0x43      |         f,f->f            |
| InvertF    | 0x44      |           f->f            |
| Float comparison: | | |
| EqualsF    | 0x4A      |         f,f->b            |
| !EqualsF   | 0x4B      |         f,f->b            |
| GreaterF   | 0x4C      |         f,f->b            |
| LessF      | 0x4D      |         f,f->b            |
| GreaterEqF | 0x4E      |         f,f->b            |
| LessEqF    | 0x4F      |         f,f->b            |
| String operations: | | |
| ConcatS    | 0x50      |         s,s->s            |
| RepeatS    | 0x51      |         s,i->s            | "ab" * 4 == "abababab"
| LengthS    | 0x52      |           s->i            |
| String comparison: | | |
| EqualsS    | 0x5A      |         s,s->b            |
| !EqualsS   | 0x5B      |         s,s->b            |
| GreaterS   | 0x5C      |         s,s->b            |
| LessS      | 0x5D      |         s,s->b            |
| GreaterEqS | 0x5E      |         s,s->b            |
| LessEqS    | 0x5F      |         s,s->b            |
| Logical operations: | | |
| Not        | 0x6A      |           b->b            |
| And        | 0x6B      |         b,b->b            |
| Or         | 0x6C      |         b,b->b            |
| Conversion: | | |
| itof       | 0x70      |           i->f            |
| ftoi       | 0x71      |           f->i            |
| itos       | 0x72      |           i->s            |
| stoi       | 0x73      |           s->i            |
| ftos       | 0x74      |           f->s            |
| stof       | 0x75      |           s->f            |
| Stuff: | | |
| If         | 0x75      |         b,i->             | Pops a1, a2, if(a1) Goto a2
| Goto       | 0x75      |           i->             | Pops 1 adress, jumps
| Exit       | 0xA1      |            ->             | Exits program, should be at the end
| Read       | 0xA2      |            ->s            | Pushes read value
| WriteI     | 0xA3      |           i->i            | does NOT pops value
| WriteF     | 0xA4      |           f->f            | 
| WriteB     | 0xA5      |           b->b            | 
| WriteS     | 0xA6      |           s->s            | 