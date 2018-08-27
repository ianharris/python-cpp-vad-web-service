#ifndef __PYTHON_LIBFVAD_LIBFVAD_MODULE_H__
#define __PYTHON_LIBFVAD_LIBFVAD_MODULE_H__

#include <fvad.h>

class VADProcessor
{
private:
    Fvad *fvad;
public:
    VADProcessor();
    ~VADProcessor();

    // setter for the underlying fvad instance's sample rate
    int setSampleRate(int rate);
    // setter for the underlying fvad instance's mode
    int setMode(int mode);

    // process audio
    int process(int16_t *frame, 
                size_t length);
};

#endif

