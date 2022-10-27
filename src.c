#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void lecteurTrame (char* nomfic, char* offset, char* destination, char* source, char* type, char* data)
{
    FILE file = fopen(nomfic, "r");
    if(file == NULL)
    {
        printf("Erreur de lecture du fichier : %s\n", nomfic);
    }

    char ligne[255];
    char* offSet = (char*) malloc( 95 * sizeof(char) );
    char* dest = (char*) malloc( 6 * sizeof(char) );
    char* src = (char*) malloc( 6 * sizeof(char) );
    char* t = (char*) malloc( 2 * sizeof(char) );
    char* dat = (char*) malloc( 1500 * sizeof(char) );
    if(fgets(ligne, 255, file) != NULL)
    {
        sscanf(ligne,"%s   %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s", offSet[0], 
            dest[0], dest[1], dest[2], dest[3], dest[4], dest[5],
            src[0], src[1], src[2], src[3], src[4], src[5],
            t[0], t[1],
            dat[0], dat[1]);
    }
    int i1 = 1;
    int i2 = 2;
    while(fgets(ligne, 255, file) != NULL)
    {
        sscanf(ligne,"%s   %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s", offSet[i1++],
            dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++],
            dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++], dat[i2++]);
    }

    offset = offSet;
    source = src;
    destination = dest;
    type = t;
    data = dat;
}

int main()
{
    char* offSet = NULL;
    char* dest = NULL;
    char* src = NULL;
    char* t = NULL;
    char* dat = NULL;
    lecteurTrame("tcp.txt", offSet, dest, src, t, dat);
    printf("offset : %s\n", offSet);
    printf("dest : %s\n", dest);
    printf("src : %s\n", src);
    printf("type : %s\n", t);
    printf("data : %s\n", dat);

    return 0;
}
