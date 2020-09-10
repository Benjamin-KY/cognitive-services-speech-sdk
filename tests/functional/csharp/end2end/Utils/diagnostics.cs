//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
//

using System;
using Microsoft.CognitiveServices.Speech.Test.Internal;
using static Microsoft.CognitiveServices.Speech.Test.Internal.SpxExceptionThrower;
using Microsoft.CognitiveServices.Speech.Internal;
using System.Globalization;
using System.Runtime.InteropServices;
using System.Runtime.CompilerServices;
using System.IO;
using System.Text;

namespace Microsoft.CognitiveServices.Speech.Test
{
    /// <summary>
    /// Diagnostics access for internal objects.
    /// </summary>
    public class Diagnostics
    {
        // Hold the callback to prevent it from being GC'd.
        private static LogMessageCallbackFunctionDelegate callback;

        private static readonly Object lockObj = new object();

        /// <summary>
        /// Sets a callback to receive all internal log lines.
        /// </summary>
        /// <param name="callback">Callback to be invoked</param>
        /// <returns>VOID!</returns>
        public static void SetLogMessageCallback(LogMessageCallbackFunctionDelegate callback)
        {
            lock (lockObj)
            {
                ThrowIfFail(Internal.Diagnostics.diagnostics_logmessage_set_callback(callback));
                Diagnostics.callback = callback;
            }
        }

        /// <summary>
        /// Sets filter criteria for all logging.
        /// </summary>
        /// <param name="filters">';' delimited list of filters.</param>
        /// <returns>VOID!</returns>
        public static void SetLogMessageFilter(string filters)
        {
            ThrowIfFail(Internal.Diagnostics.diagnostics_logmessage_set_filters(filters));
        }

        public static void StartMemoryLogging()
        {
            Internal.Diagnostics.diagnostics_log_memory_start_logging();
        }

        public static void StopMemoryLogging()
        {
            Internal.Diagnostics.diagnostics_log_memory_stop_logging();
        }

        public static void DumpMemoryLogToFile(string fileName, int options)
        {
            bool stdOut = (options & 2) == 2;
            bool stdErr = (options & 4) == 4 || (fileName == null && options == 0);
            if ((stdOut || stdErr) && fileName == null)
            {
                fileName = "CRBN";
            }

            var sw = (options & 1) == 1 && !string.IsNullOrEmpty(fileName)
                ? new StreamWriter(File.Open(fileName, FileMode.Create), Encoding.UTF8)
                : null;

            var start = Internal.Diagnostics.diagnostics_log_memory_get_line_num_oldest();
            var stop = Internal.Diagnostics.diagnostics_log_memory_get_line_num_newest();
            for (var i = start; i <= stop; i++)
            {
                var linePtr = Internal.Diagnostics.diagnostics_log_memory_get_line(i);
                var line = Marshal.PtrToStringAnsi(linePtr);

                if (stdOut) Console.Write($"{fileName}: {line}");
                if (stdErr) Console.Error.Write($"{fileName}: {line}");

                if (sw != null) sw.Write($"CRBN: {line}");
            }

            sw?.Close();
            sw?.Dispose();
        }

        public static object[] Args(params object[] args)
        {
            return args;
        }

        public static void SPX_TRACE_INFO(string message, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            SPX_TRACE_INFO(message, Args(), line, caller, file);
        }

        public static void SPX_TRACE_WARNING(string message, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            SPX_TRACE_WARNING(message, Args(), line, caller, file);
        }

        public static void SPX_TRACE_ERROR(string message, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            SPX_TRACE_ERROR(message, Args(), line, caller, file);
        }

        public static void SPX_TRACE_VERBOSE(string message, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            SPX_TRACE_VERBOSE(message, Args(), line, caller, file);
        }

        public static void SPX_TRACE_INFO(string format, object[] args, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            var message = string.Format(format, args);
            Internal.Diagnostics.diagnostics_log_trace_string(Internal.Diagnostics.__SPX_TRACE_LEVEL_INFO, "SPX_TRACE_INFO", file, line, message);
        }

        private static void SPX_TRACE_WARNING(string format, object[] args, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            var message = string.Format(format, args);
            Internal.Diagnostics.diagnostics_log_trace_string(Internal.Diagnostics.__SPX_TRACE_LEVEL_WARNING, "SPX_TRACE_WARNING", file, line, message);
        }

        private static void SPX_TRACE_ERROR(string format, object[] args, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            var message = string.Format(format, args);
            Internal.Diagnostics.diagnostics_log_trace_string(Internal.Diagnostics.__SPX_TRACE_LEVEL_ERROR, "SPX_TRACE_ERROR", file, line, message);
        }

        private static void SPX_TRACE_VERBOSE(string format, object[] args, [CallerLineNumber]int line = 0, [CallerMemberName]string caller = null, [CallerFilePath]string file = null)
        {
            var message = string.Format(format, args);
            Internal.Diagnostics.diagnostics_log_trace_string(Internal.Diagnostics.__SPX_TRACE_LEVEL_VERBOSE, "SPX_TRACE_VERBOSE", file, line, message);
        }
    }
}
