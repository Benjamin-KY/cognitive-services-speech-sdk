//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
//
// speechapi_cxx_recognition_base_async_recognizer.h: Public API declarations for BaseAsyncRecognizer C++ class
//

#pragma once
#include <future>
#include <memory>
#include <speechapi_cxx_common.h>
#include <speechapi_cxx_eventsignal.h>
#include <speechapi_cxx_session_eventargs.h>
#include <speechapi_cxx_recognition_base_async_recognizer.h>


namespace CARBON_NAMESPACE_ROOT {
namespace Recognition {


class BaseAsyncRecognizer : public AsyncRecognizer<RecognitionResult, RecognitionEventArgs>
{
public:

    using BaseType = AsyncRecognizer<RecognitionResult, RecognitionEventArgs>;
    
    BaseAsyncRecognizer(SPXRECOHANDLE hreco) :
        BaseType(hreco)
    {
    }

    template <class T>
    static std::shared_ptr<BaseAsyncRecognizer> FromRecognizer(const std::shared_ptr<T> &recognizer) 
    {
        UNUSED(recognizer);
        SPX_STATIC_ASSERT_IS_BASE_OF(Recognizer, T);
        return nullptr;
    }

protected:

    BaseAsyncRecognizer() = default;
    BaseAsyncRecognizer(BaseAsyncRecognizer&&) = delete;
    BaseAsyncRecognizer(const BaseAsyncRecognizer&) = delete;
    BaseAsyncRecognizer& operator=(BaseAsyncRecognizer&&) = delete;
    BaseAsyncRecognizer& operator=(const BaseAsyncRecognizer&) = delete;
};


} } // CARBON_NAMESPACE_ROOT :: Recognition
