//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
//
// speechapi_cxx_recognition_eventargs.h: Public API declarations for RecognitionEventArgs C++ base class
//

#pragma once
#include <string>
#include <speechapi_cxx_common.h>


namespace CARBON_NAMESPACE_ROOT {
namespace Recognition {


class RecognitionEventArgs : public SessionEventArgs
{
public:

    RecognitionEventArgs(SPXEVENTHANDLE hevent = SPXHANDLE_INVALID) :
        SessionEventArgs(hevent)
    {
    };


public:

    RecognitionEventArgs(RecognitionEventArgs&&) = delete;
    RecognitionEventArgs(const RecognitionEventArgs&) = delete;
    RecognitionEventArgs& operator=(RecognitionEventArgs&&) = delete;
    RecognitionEventArgs& operator=(const RecognitionEventArgs&) = delete;
};


} } // CARBON_NAMESPACE_ROOT :: Recognition
