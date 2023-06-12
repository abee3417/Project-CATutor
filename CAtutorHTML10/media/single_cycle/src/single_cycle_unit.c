#include "../header/CPU/cpu.h"
#include "../header/bit_functions/bit_functions.h"
#include "../header/logic_gates/logic_gates.h"
#include "../header/memory/memory.h"

#include<stdio.h>
#include<string.h>

int main(int argc, char* argv[]){
	reg[29] = 0x01000000;
	reg[31] = 0xffffffff;
    
	FILE* file = fopen(argv[1], "r");
	CPU cpu;
	int i = 0;
	while(fgets(mem+i, 5, file) != NULL){
		i+=4;
	}
    fclose(file);
    
    char s1[100];

    sprintf(s1, "%s.json", argv[1]);    // "Hello, %s"로 서식을 지정하여 s1에 저장
        
	freopen(s1, "w", stdout);
    printf("{\"total\": [{\"cycle\": 0, \"pc\": \"0x%x\", \"ir\": \"0x00000000\"", pc);
    for (int i = 0; i<32; i++){
        printf(", \"reg[%d]\": \"0x%x\"", i, reg[i]);
    }
    printf("}\n");
    
	while (pc != 0xffffffff){
		fetch(&cpu, mem);
		decode(&cpu);
		execute(&cpu);
		memory_operation(&cpu, mem);
		write_back(&cpu, mem);
		pc_update(&cpu);
        print_result();
	}
    printf("]}");
	//print_result();
    fclose(stdout);
    
	return 0;
}