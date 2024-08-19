from flask import Flask, render_template, request, send_from_directory
import matplotlib.pyplot as plt
import numpy as np
import os

def crear_app():
    app = Flask(__name__)

    # Crear el directorio de gráficos si no existe
    os.makedirs('static/plots', exist_ok=True)

    @app.route("/", methods=["GET", "POST"])
    def index():
        plot_file = None
        if request.method == "POST":
            try:
                # Obtener los coeficientes de la ecuación lineal de la forma y = mx + b
                m = float(request.form.get("m"))
                b = float(request.form.get("b"))

                # Generar puntos para la gráfica
                x = np.linspace(-10, 10, 400)
                y = m * x + b

                # Crear la gráfica
                plt.figure()
                plt.plot(x, y, label=f'y = {m}x + {b}', color='blue')
                plt.axhline(0, color='black', linewidth=0.5, ls='--')
                plt.axvline(0, color='black', linewidth=0.5, ls='--')
                plt.title('Gráfica de la Ecuación Lineal')
                plt.xlabel('x')
                plt.ylabel('y')
                plt.grid()
                plt.legend()

                # Guardar la imagen
                plot_file = 'static/plots/plot.png'
                plt.savefig(plot_file)
                plt.close()

            except Exception as e:
                return str(e)

        return render_template("index.html", plot_file=plot_file)

    @app.route('/plots/<path:filename>')
    def send_plot(filename):
        return send_from_directory('static/plots', filename)

    return app

if __name__ == "__main__":
    app = crear_app()  # Crear la instancia de la aplicación
    app.run(debug=True)  # Ejecutar la aplicación
