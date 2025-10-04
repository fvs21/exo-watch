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
        <div className="kicker">Mision: Data Science</div>
        <h1 className="hero__title">
          ML exoplanet detection
        </h1>
        <p className="hero__subtitle">
          Load a CSV, tune your model, and generate synthetic star systems.
          Visualize key metrics and estimate habitability with a reproducible
          pipeline.
        </p>
        <div className="actions">
          <button className="btn primary" onClick={() => setVista("ingresar")}>
            Start
          </button>
          <button className="btn ghost" onClick={() => setVista("hparams")}>
            Settings
          </button>
        </div>
        <ul className="hero__bullets" aria-label="Características">
          <li>⚡ Data → Model → Prediction</li>
          <li>🧪 Syntetic Data Generator</li>
          <li>📊 Demo ready metrics</li>
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
            ⚙️ Tune your model
          </button>
          <button className="btn primary" onClick={() => setVista("ingresar")}>
            🚀 Classify data
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
            <span className="badge">Technical Demo</span>
          </div>

          <nav className="footer__links" aria-label="Navegación secundaria">
            <button className="linkLike" onClick={() => setVista("menu")}>
              Start
            </button>
            <button className="linkLike" onClick={() => setVista("hparams")}>
              Hyperparameters
            </button>
            <button className="linkLike" onClick={() => setVista("ingresar")}>
              Classify data
            </button>
            <a href="https://github.com/" target="_blank" rel="noreferrer">
              GitHub
            </a>
          </nav>

          <div className="footer__legal">
            <p className="muted">
              © {new Date().getFullYear()} ExoScope · Exoplanet detection project —
              <span className="muted strong">
                {" "}
                Developed for a hackathon environment (unofficial NASA)
              </span>
            </p>
            <p className="micro">
              This software is for demonstration and research purposes. It does
              not represent official scientific endorsement.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
