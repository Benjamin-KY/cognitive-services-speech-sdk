# Copyright (c) Microsoft. All rights reserved.
# See https://aka.ms/csspeech/license201809 for the full license information.

import pytest
import os
from collections import namedtuple
from typing import Callable

import azure.cognitiveservices.speech as msspeech
from .utils import _setup_callbacks


def pytest_addoption(parser):
    parser.addoption("--inputdir")
    parser.addoption("--subscription")
    parser.addoption("--speech-region")
    parser.addoption("--luis-subscription")
    parser.addoption("--luis-region")
    parser.addoption("--endpoint", help="Specify an endpoint. Currently only used for speech reco.")
    parser.addoption("--host", help="Specify a host. Format is protocol://host:port where :port is optional.")
    parser.addoption("--language-understanding-app-id")
    parser.addoption('--no-use-default-microphone', action='store_true', dest="no_use_default_microphone",
                     default=False, help="disable tests that require a default microphone")


@pytest.fixture
def subscription(request):
    return request.config.getoption("--subscription")


@pytest.fixture
def luis_subscription(request):
    return request.config.getoption("--luis-subscription")


@pytest.fixture
def speech_region(request):
    return request.config.getoption("--speech-region")


@pytest.fixture
def luis_region(request):
    return request.config.getoption("--luis-region")


@pytest.fixture
def endpoint(request):
    """specify an endpoint. If given, it overrides the region settings for speech recognizers."""
    return request.config.getoption("--endpoint")


@pytest.fixture
def host(request):
    """specify a host. If given, it overrides the region settings for speech recognizers."""
    return request.config.getoption("--host")


@pytest.fixture
def default_speech_auth(subscription, speech_region, endpoint, host):
    # if an endpoint or a host is given, it overrides the set region
    region = speech_region if not endpoint and not host else None

    return {'endpoint': endpoint,
            'host': host,
            'subscription': subscription,
            'region': region}


@pytest.fixture
def language_understanding_app_id(request):
    return request.config.getoption("--language-understanding-app-id")


@pytest.fixture
def skip_default_microphone(request):
    no_use_default_microphone = request.config.getoption("--no-use-default-microphone")
    if no_use_default_microphone:
        pytest.skip('skipping without default microphone')


SpeechInput = namedtuple('SpeechInputData',
                         ('path', 'transcription', 'offset', 'duration', 'input_language', 'translations'))

batman_offsets, batman_durations = zip(*[
    (5400000, 145300000),
    (156400000, 144400000),
    (229200000, 200000000),
    (440500000, 200000000),
    (648500000, 41900000),
    (708000000, 68600000),
    (788700000, 200000000),
    (996700000, 113000000),
    (1151900000, 200000000),
    (1359900000, 6200000),
    (1375800000, 200000000),
    (1587100000, 200000000),
    (1795100000, 41900000),
    (1854600000, 68600000),
    (1935300000, 200000000),
    (2143300000, 113000000)])

speech_input_data_raw = {'weather':
                         ('whatstheweatherlike.wav', ["What's the weather like?"], (200000, ),
                          (16000000, ), 'en-US',
                          {'fr': "Quel temps fait-il ?",
                           'de': "Wie ist das Wetter?"}
                          ),
                         'lamp': ('TurnOnTheLamp.wav', ["Turn on the lamp."], (3300000, ),
                                  (15700000, ), 'en-US', dict()),
                         'silence': ('silenceshort.wav', [''], None, None, 'en-US', dict()),
                         'silencehello': ('silencehello.wav', ['Hello.'], None, None, 'en-US', dict()),
                         'batman': ('batman.wav', [
                                "Skills and abilities Batman has no inherent super powers, he relies on his own scientific knowledge detective skills and athletic prowess in the stories. Batman is regarded as one of the world's greatest detective if not the world's greatest crime solver. Batman has been repeatedly described as having genius level intellect. One of the greatest martial artists in the DC universe.",
                                "And having peak human physical conditioning, he has traveled the world, acquiring the skills needed to aid his cruceta grants crime.",
                                "His knowledge and expertise in almost every discipline known to man is nearly unparalleled by any other character in the universe.",
                                "Batman's inexhaustible wealth allows him to access advanced technology as a proficient scientist is able to use and modify those technologies to his advantage.",
                                "Batman describes Superman as the most dangerous man on Earth able to defeat a team of super powered extraterrestrials by himself in order to rescue his imprisoned teammates.",
                                "In the 1st storyline, Superman also considers Batman to be one of the most brilliant minds on the planet.",
                                "Batman has the ability to function under great physical pain and withstand mind control. He is a master of disguise multilingual and an expert in espionage, often gathering information under different identity's.",
                                "Batman's Karate Judo and jujitsu training has made him a math master of stealth an escape, allowing too much allowing him to appear and disappear at Will and to break free."
                         ], batman_offsets, batman_durations, 'en-US', dict()),
                         'beach': ('wreck-a-nice-beach.wav', ["Wreck a nice beach."], (1700000,), (10800000,), 'en-us', dict()),
                         'beach_nohelp': ('wreck-a-nice-beach.wav', ["Recognize speech."], (1000000,), (17500000,), 'en-us', dict()),
                         'beach_nohelp_truman': ('wreck-a-nice-beach.wav', ["Recognize speech."], (1700000,), (10800000,), 'en-us', dict())}


@pytest.fixture
def speech_input(request):
    inputdir = request.config.getoption("--inputdir")

    try:
        filename, *args = speech_input_data_raw[request.param]
    except AttributeError:
        # don't fail if no request is given, so that speech_input can be overridden by kws_input
        return None

    path = os.path.join(inputdir, filename)
    return SpeechInput(path, *args)


IntentInput = namedtuple('IntentInputData',
                         ('path', 'transcription', 'offset', 'duration', 'intent_id'))
intent_input_data_raw = {
    'lamp': ('TurnOnTheLamp.wav', ["Turn on the lamp."], (3800000, ), (11200000, ),
             'HomeAutomation.TurnOn'),
    'beach': ('wreck-a-nice-beach.wav', ["Wreck a nice beach."], (1700000,),
              (10800000,), None),
    'beach_nohelp': ('wreck-a-nice-beach.wav', ["Recognize speech."],
                     (1000000,), (17500000,), None),
    'beach_nohelp_truman': ('wreck-a-nice-beach.wav', ["Recognize speech."],
                            (1700000,), (10800000,), None)}


@pytest.fixture
def intent_input(request):
    inputdir = request.config.getoption("--inputdir")

    filename, *args = intent_input_data_raw[request.param]
    path = os.path.join(inputdir, filename)
    return IntentInput(path, *args)


KwsInput = namedtuple('KwsInputData',
                      ('path', 'transcription', 'offset', 'duration', 'model_file', 'model_keyword'))

kws_input_data_raw = {
    'computer': ('kws_whatstheweatherlike.wav', [
        "Computer what's the weather like?"],
        (None, ),
        (None, ),
        ('Computer', 'kws.table'),
        "",
    ),
}


@pytest.fixture
def kws_input(request):
    inputdir = request.config.getoption("--inputdir")

    try:
        args = dict(zip(KwsInput._fields, kws_input_data_raw[request.param]))
    except AttributeError:
        # don't fail if no request is given, so that kws_input can be empty
        return None

    audiopath = os.path.join(inputdir, '..', 'kws', args['path'])
    kwspath = os.path.join(inputdir, '..', 'kws', *args['model_file'])
    return KwsInput(audiopath, args['transcription'], args['offset'], args['duration'],
                    kwspath, args['model_keyword'])


@pytest.fixture
def from_file_speech_reco_with_callbacks(speech_input: SpeechInput, kws_input: KwsInput,
        default_speech_auth):
    """
    Fixture to generate a `SpeechRecognizer` setup with audio input from file as defined by
    `speech_input` or `kws_input` and subscription information.

    @return: A function that takes a function `setup_callback_handle` to setup callbacks on the
        recognizer, and key word arguments which override subscription information. It returns a
        tuple `(recognizer, callbacks)`.
    """
    speech_input = speech_input or kws_input

    def build_recognizer(setup_callback_handle: Callable = _setup_callbacks, **kwargs):
        audio_config = msspeech.audio.AudioConfig(filename=speech_input.path)
        speech_config = msspeech.SpeechConfig(
            subscription=kwargs.get('subscription', default_speech_auth['subscription']),
            region=kwargs.get('speech_region', default_speech_auth['region']),
            endpoint=kwargs.get('endpoint', default_speech_auth['endpoint']),
            host=kwargs.get('host', default_speech_auth['host']))

        reco = msspeech.SpeechRecognizer(speech_config, audio_config)
        callbacks = setup_callback_handle(reco)

        return (reco, callbacks)

    return build_recognizer


@pytest.fixture
def from_file_translation_reco_with_callbacks(subscription: str, speech_input: SpeechInput,
                                              speech_region: str):
    """
    Fixture to generate a `TranslationRecognizer` setup with audio input from file as defined by
    `speech_input` and subscription information.

    @return: A function that takes a function `setup_callback_handle` to setup callbacks on the
        recognizer, and key word arguments which override subscription information. It returns a
        tuple `(recognizer, callbacks)`.
    """
    def build_recognizer(setup_callback_handle: Callable = _setup_callbacks, **kwargs):
        audio_config = msspeech.audio.AudioConfig(filename=speech_input.path)
        translation_config = msspeech.translation.SpeechTranslationConfig(
            subscription=kwargs.get('subscription', subscription),
            region=kwargs.get('speech_region', speech_region),
            endpoint=kwargs.get('endpoint', None),
            host=kwargs.get('host', None))

        translation_config.speech_recognition_language = speech_input.input_language
        for language in speech_input.translations:
            translation_config.add_target_language(language)

        translation_config.voice_name = "de-DE-Hedda"

        reco = msspeech.translation.TranslationRecognizer(translation_config, audio_config)
        callbacks = setup_callback_handle(reco)

        return (reco, callbacks)

    return build_recognizer


@pytest.fixture
def from_file_intent_reco_with_callbacks(luis_subscription: str, intent_input: IntentInput,
                                         luis_region: str, language_understanding_app_id: str):
    """
    Fixture to generate a `IntentRecognizer` setup with audio input from file as defined by
    `speech_input` and subscription information.

    @return: A function that takes a function `setup_callback_handle` to setup callbacks on the
        recognizer, and key word arguments which override subscription information. It returns a
        tuple `(recognizer, callbacks)`.
    """
    def build_recognizer(setup_callback_handle: Callable = _setup_callbacks, **kwargs):
        audio_config = msspeech.audio.AudioConfig(filename=intent_input.path)
        speech_config = msspeech.SpeechConfig(
            subscription=kwargs.get('subscription', luis_subscription),
            region=kwargs.get('luis_region', luis_region),
            endpoint=kwargs.get('endpoint', None),
            host=kwargs.get('host', None))

        reco = msspeech.intent.IntentRecognizer(speech_config, audio_config)

        model = msspeech.intent.LanguageUnderstandingModel(app_id=language_understanding_app_id)
        reco.add_intent(model, "HomeAutomation.TurnOn")
        reco.add_intent(model, "HomeAutomation.TurnOff")

        reco.add_intent("This is a test.", "test")
        reco.add_intent("Switch the to channel 34.", "34")
        reco.add_intent("what's the weather like", "weather")

        callbacks = setup_callback_handle(reco)

        return (reco, callbacks)

    return build_recognizer

