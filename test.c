#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <wiringPiSPI.h>

#define CHANNEL 0

uint8_t snow[] = {
			0,    //00000000
			40,   //00101000
			146,  //10010010
			84,   //01010100
			40,   //00101000
			84,   //01010100
			146,  //10010010
			40    //00101000
		};

uint8_t buf[2];

void spi(uint8_t reg, uint8_t val) {
	buf[0] = reg;
	buf[1] = val;
	wiringPiSPIDataRW(CHANNEL, buf, 10);
}

void show() {
	for(int i=0; i < 8; i++) { //in rows
		spi(i+1,(char)(snow[i]));
	}
}

void clear() {
	for (int i = 0; i < 8; ++i) {
		spi(i+1, 0);
	}
}

void setupLEDMatrix(int channel) {
	if (wiringPiSPISetup(CHANNEL, 1000000) < 0) {
		fprintf (stderr, "SPI Setup failed: %s\n", strerror (errno));
		exit(errno);
	}

	spi(0x09,0x00); //decode mode
	spi(0x0B,0x07); //scan limit
	spi(0x0A,0xF3); //brightness
	spi(0x0C,0x01); //shutdown mode
	spi(0x0F,0x00); //test mode
}

int main(int argc, char** argv) {
	setupLEDMatrix(CHANNEL);
	clear();
	show();
	sleep(3);
	clear();
	return 0;
}
