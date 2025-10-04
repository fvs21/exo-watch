import { useState } from "react";
import IngresarDatos from "./views/ingresarDatos";
import Hparams from "./views/hparams";
import exoplanetasImg from "./assets/exoplanetas.jpeg";
import "./styles/app.css";

type Vista = "menu" | "ingresar" | "hparams";

function MainPage({ setVista }: { setVista: (v: Vista) => void }) {
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

export default function App() {
  const [vista, setVista] = useState<Vista>("menu");

  return (
    <div
      className="landing"
      style={{
        ["--hero-img" as any]: `url(${exoplanetasImg})`,
      }}
    >
      <header className="nav">
        <button
          className="brand"
          onClick={() => setVista("menu")}
          aria-label="ExoScope"
        >
          <span className="logo" aria-hidden>
            ✦
          </span>
          <span className="brandText">ExoScope</span>
        </button>
        <div className="navActions">
          <button className="btn" onClick={() => setVista("hparams")}>
            ⚙️ Ajusta tu modelo
          </button>
          <button className="btn primary" onClick={() => setVista("ingresar")}>
            🚀 Ingresar datos
          </button>
        </div>
      </header>
      {vista === "menu" && <MainPage setVista={setVista} />}
      {vista === "ingresar" && <IngresarDatos setVista={setVista} />}
      {vista === "hparams" && <Hparams setVista={setVista} />}

      <footer className="footer" role="contentinfo">
        <div className="footer__content container">
          <div className="footer__brand">
            <span className="logo" aria-hidden>
              ✦
            </span>
            <span className="brandText">ExoScope</span>
            <span className="divider" aria-hidden>
              •
            </span>
            <span className="badge">Demo técnica</span>
          </div>

          <nav className="footer__links" aria-label="Navegación secundaria">
            <button className="linkLike" onClick={() => setVista("menu")}>
              Inicio
            </button>
            <button className="linkLike" onClick={() => setVista("hparams")}>
              Hiperparámetros
            </button>
            <button className="linkLike" onClick={() => setVista("ingresar")}>
              Ingresar datos
            </button>
            <a href="https://github.com/" target="_blank" rel="noreferrer">
              GitHub
            </a>
          </nav>

          <div className="footer__legal">
            <p className="muted">
              © {new Date().getFullYear()} ExoScope · Proyecto de detección de
              exoplanetas —
              <span className="muted strong">
                {" "}
                Desarrollado para un entorno de hackatón (no oficial de NASA)
              </span>
            </p>
            <p className="micro">
              Este software es para fines demostrativos y de investigación. No
              representa recomendación científica oficial.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
