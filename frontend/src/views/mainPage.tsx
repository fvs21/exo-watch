import exoplanetasImg from "../assets/exoplanetas.jpg";
import "../styles/app.css";

type Props = {
  setVista: (v: "menu" | "ingresar" | "hparams") => void; // <- ACEPTA setVista
};

export default function MainPage() {
  return (
    <section className="hero" role="banner">
      <div className="hero__backdrop" />
      <div className="container hero__content">
        <div className="kicker">Misión: Ciencia de Datos</div>
        <h1 className="hero__title">
          Detección de <span className="accent">exoplanetas</span> asistida por
          IA
        </h1>
        <p className="hero__subtitle">
          Carga un CSV, ajusta tu modelo y genera sistemas estelares simulados.
          Visualiza métricas clave y estima habitabilidad con un pipeline
          reproducible.
        </p>
        <div className="actions">
          <button className="btn primary" onClick={() => setVista("ingresar")}>
            Comenzar
          </button>
          <button className="btn ghost" onClick={() => setVista("hparams")}>
            Configuración
          </button>
        </div>
        <ul className="hero__bullets" aria-label="Características">
          <li>⚡ Datos → Modelo → Predicción</li>
          <li>🧪 Generador de sistemas sintéticos</li>
          <li>📊 Métricas listas para demo</li>
        </ul>
      </div>
    </section>
  );
}
