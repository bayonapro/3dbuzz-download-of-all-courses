#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>

int main()
{
    while(1) {
        if (fork() == 0) {
            execlp("python3", "python3", "bayonaload.py", (char *)NULL);
        } else {
            waitpid(-1, NULL, 0);
            printf("-----------------------------------------------\n");
        }
    }
    return 0;
}