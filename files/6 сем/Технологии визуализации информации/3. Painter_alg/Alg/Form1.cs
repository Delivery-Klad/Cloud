using System;
using System.Drawing;
using System.Windows.Forms;
using System.Numerics;

namespace WindowsFormsApplication2
{
    public partial class Form1 : Form
    {
        Bitmap buffer;
        Graphics gfx;

        public Form1()
        {
            InitializeComponent();
            buffer = new Bitmap(pictureBox1.Width, pictureBox1.Height);
            gfx = Graphics.FromImage(buffer);
        }
        struct Vertex
        {
            public Vector4 position;
            public Color color;
            public Vector3 normal;
        }

        Vertex[,] back1 = new Vertex[,] {{ new Vertex {position = new Vector4(-5,-5, 0,1),  color = Color.Blue, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4( 5,-5, 0,1),  color = Color.Blue, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4(-5, 5, 0,1),  color = Color.Blue, normal = new Vector3(0,0,-1)} },
                                         { new Vertex {position = new Vector4( 5,-5, 0,1),  color = Color.Blue, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4( 5, 5, 0,1),  color = Color.Blue, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4(-5, 5, 0,1),  color = Color.Blue, normal = new Vector3(0,0,-1)} }};
        Vertex[,] back2 = new Vertex[,] {{ new Vertex {position = new Vector4(-5,-5, 0,1),  color = Color.Gray, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4( 5,-5, 0,1),  color = Color.Gray, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4(-5, 5, 0,1),  color = Color.Gray, normal = new Vector3(0,0,-1)} },
                                         { new Vertex {position = new Vector4( 5,-5, 0,1),  color = Color.Gray, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4( 5, 5, 0,1),  color = Color.Gray, normal = new Vector3(0,0,-1)},
                                           new Vertex {position = new Vector4(-5, 5, 0,1),  color = Color.Gray, normal = new Vector3(0,0,-1)} }};

        private Vertex[,] ApplyTransform(Vertex[,] model, Matrix4x4 transform)
        {
            Vertex[,] mdl = (Vertex[,])model.Clone();
            for (int pindex = 0; pindex < model.GetLength(0); pindex++)
            {
                for (int i = 0; i < model.GetLength(1); i++)
                {
                    mdl[pindex, i].position = Vector4.Transform(mdl[pindex, i].position, transform);
                    mdl[pindex, i].normal = Vector3.TransformNormal(mdl[pindex, i].normal, transform);
                }
            }
            return mdl;
        }

        private Vertex[,] Aggregate(Vertex[,] model1, Vertex[,] model2)
        {
            Vertex[,] result = new Vertex[model1.GetLength(0) + model2.GetLength(0), model1.GetLength(1)];

            int index = 0;
            for (int i = 0; i < model1.GetLength(0); i++, index++)
            {
                for (int j = 0; j < model1.GetLength(1); j++)
                {
                    result[index, j] = model1[i, j];
                }
            }
            for (int i = 0; i < model2.GetLength(0); i++, index++)
            {
                for (int j = 0; j < model2.GetLength(1); j++)
                {
                    result[index, j] = model2[i, j];
                }
            }
            return result;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            Matrix4x4 projection = Matrix4x4.CreatePerspectiveFieldOfView((float)(Math.PI / 3.0), (float)buffer.Width / buffer.Height, 1.0f, 100.0f);
            Matrix4x4 windowScale = Matrix4x4.CreateScale(buffer.Width / 2, -buffer.Height / 2, 1.0f) * Matrix4x4.CreateTranslation(buffer.Width / 2, buffer.Height / 2, 0.0f);

            gfx.FillRectangle(new SolidBrush(Color.Black), new Rectangle(0, 0, buffer.Width, buffer.Height));

            Vertex[,] b1 = ApplyTransform(back1, Matrix4x4.CreateRotationX((float)(trackBar1.Value * Math.PI / 180.0)) * Matrix4x4.CreateTranslation(0.0f, 1.0f, -8.0f) * projection * windowScale);
            Vertex[,] b2 = ApplyTransform(back2, Matrix4x4.CreateRotationX((float)(trackBar1.Value * Math.PI / 180.0)) * Matrix4x4.CreateTranslation(0.0f, -1.0f, -8.0f) * projection * windowScale);
            
            DrawModel(Aggregate(b1, b2));
            pictureBox1.Image = buffer;
        }

        private void DrawModel(Vertex[,] model)
        {
            Point[] poly = new Point[3];
            for (int pindex = 0; pindex < model.GetLength(0); pindex++)
            {
                for (int i = 0; i < model.GetLength(1); i++)
                {
                    poly[i].X = (int)(model[pindex, i].position.X / model[pindex, i].position.W);
                    poly[i].Y = (int)(model[pindex, i].position.Y / model[pindex, i].position.W);
                }
                gfx.FillPolygon(new SolidBrush(model[pindex, 0].color), poly);
            }
        }
    }
}

