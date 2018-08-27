#include <iostream>

#include "libfvad_module.h"

VADProcessor::VADProcessor()
{
    fvad = fvad_new();
    if(!fvad) {
        std::cout << "An error occurred allocating an fvad object" << std::endl;
    }
}

VADProcessor::~VADProcessor()
{
    fvad_free(fvad);
}

int VADProcessor::setSampleRate(int rate)
{
    return fvad_set_sample_rate(fvad,
                                rate);
}

int VADProcessor::setMode(int mode)
{
    return fvad_set_mode(fvad, 
                         mode);
}

int VADProcessor::process(int16_t *frame,
                          size_t length)
{
    return fvad_process(fvad,
                        frame,
                        length);
}

