using System;
using System.Buffers.Text;
using System.Text;
using NetMQ;
using NetMQ.Sockets;
using Newtonsoft.Json;

namespace zmq.subscriber
{
    public class Detection
    {
        public string id { get; set; }
        public string? type { get; set; }
        public string? description { get; set; }
        public DetectionPosition? position { get; set; }
        public float? score { get; set; }
        public float? velocity { get; set; }
        public float? timestampUtm { get; set; }
    }

    public class DetectionPosition
    {
        public int? x { get; set; }
        public int? y { get; set; }
        public int? box_top_x { get; set; }
        public int? box_top_y { get; set; }
        public int? box_bottom_x { get; set; }
        public int? box_bottom_y { get; set; }
    }
    
    class Program
    {
        static void Main(string[] args)
        {
            using (var subSocket = new SubscriberSocket())
            {
                subSocket.Connect("tcp://127.0.0.1:2000");
                subSocket.Subscribe("");

                while (true)
                {
                    string buffer = subSocket.ReceiveFrameString(out bool more);
                    var detection = JsonConvert.DeserializeObject<Detection>(buffer);
                    var delay = DateTime.UnixEpoch.Second - detection.timestampUtm.Value;
                    Console.WriteLine($"delay {delay} " + JsonConvert.SerializeObject(detection));
                }
            }

            Console.WriteLine("Hello World!");
        }
    }
}