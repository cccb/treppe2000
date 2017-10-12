
# Trepped

Provide an UDP interface for the treppelights(R).


# Serial communication

The controllers expect the following format:
    1 Byte Command: 0x23 Send RGBW data
    1 Byte Channel: 0-15
    8 Byte RGBW data with 16 bit per channel,
                     encoded as 2 byte little endian



# UDP Protocol

    Commands:
    1 Byte Flag: 0x23 Send one channel RGBW data
                 0x42 Send a frame of RGBW data

    
    Command Payloads:
    0x23        1 Byte Channel (0-15)
                8 Byte RGBW data with 16 bit per channel (see above)

    0x42        1 Byte Flags:
                  0x00 8 Bit RGB data
                  0x01 8 Bit RGBW data
                  0x02 16 Bit RGB data

                1 Byte Frame length

                data

    

