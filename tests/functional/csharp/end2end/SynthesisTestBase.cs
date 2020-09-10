//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
//
using Microsoft.CognitiveServices.Speech.Tests.EndToEnd.Utils;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;

namespace Microsoft.CognitiveServices.Speech.Tests.EndToEnd
{
    using static Config;

    [TestClass]
    public class SynthesisTestBase : LoggingTestBase
    {
        public long EmptyWaveFileSize => 46;
        public int GuidLength => 32;
        public string DefaultLanguage => Language.EN;
        public string DefaultVoice => "Microsoft Server Speech Text to Speech Voice (en-US, AriaRUS)";
        public int MockAudioSize => 32000;
        public int MockAudioChunkSize => 3200;
        public string SsmlTemplate => "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml' xml:lang='{0}'><voice name='{1}'>{2}</voice></speak>";

        public static string subscriptionKey, region;
        public SpeechConfig restConfig;
        public SpeechConfig restHostConfig;
        public SpeechConfig uspConfig;
        public SpeechConfig uspHostConfig;
        public SpeechConfig mockConfig;
        public SpeechConfig customVoiceConfig;

        private static Config _config;

        public static void BaseClassInit(TestContext context)
        {
            LoggingTestBaseInit(context);
            _config = new Config(context);

            subscriptionKey = SubscriptionsRegionsMap[SubscriptionsRegionsKeys.UNIFIED_SPEECH_SUBSCRIPTION].Key;
            region = SubscriptionsRegionsMap[SubscriptionsRegionsKeys.UNIFIED_SPEECH_SUBSCRIPTION].Region;

            Console.WriteLine("region: " + region);
        }

        [ClassCleanup]
        public static void TestClassCleanup()
        {
            LoggingTestBaseCleanup();
        }

        [TestInitialize]
        public void BaseTestInit()
        {
            var endpoint = $"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1?TrafficType=Test";
            restConfig = SpeechConfig.FromEndpoint(new Uri(endpoint), subscriptionKey);
            var restHost = $"https://{region}.tts.speech.microsoft.com";
            restHostConfig = SpeechConfig.FromHost(new Uri(restHost), subscriptionKey);
            var uspEndpoint = $"wss://{region}.tts.speech.microsoft.com/cognitiveservices/websocket/v1?TrafficType=Test";
            uspConfig = SpeechConfig.FromEndpoint(new Uri(uspEndpoint), subscriptionKey);
            var uspHost = $"wss://{region}.tts.speech.microsoft.com";
            uspHostConfig = SpeechConfig.FromHost(new Uri(uspHost), subscriptionKey);
            mockConfig = SpeechConfig.FromSubscription("None", "None");
            mockConfig.SetProperty("CARBON-INTERNAL-UseTtsEngine-Mock", "true");
            var customVoiceRegion = SubscriptionsRegionsMap[SubscriptionsRegionsKeys.CUSTOM_VOICE_SUBSCRIPTION].Region;
            var customVoiceDeploymentId = DefaultSettingsMap[DefaultSettingKeys.CUSTOM_VOICE_DEPLOYMENT_ID];
            var customVoiceEndpoint = $"https://{customVoiceRegion}.voice.speech.microsoft.com/cognitiveservices/v1";
            customVoiceEndpoint += "?deploymentId=" + customVoiceDeploymentId;
            customVoiceConfig = SpeechConfig.FromEndpoint(new Uri(customVoiceEndpoint), SubscriptionsRegionsMap[SubscriptionsRegionsKeys.CUSTOM_VOICE_SUBSCRIPTION].Key);
            customVoiceConfig.SpeechSynthesisVoiceName = DefaultSettingsMap[DefaultSettingKeys.CUSTOM_VOICE_VOICE_NAME];
        }
    }
}
