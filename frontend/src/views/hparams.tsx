import { useState } from "react";
import "../styles/app.css";
import "../styles/hparams.css";

type HParams = {
  random_state?: number;
  learning_rate?: number;
  n_estimators?: number;
  num_leaves?: number;
  feature_fraction?: number;
  lambda_l1?: number;
  lambda_l2?: number;
};

type Props = {
  setVista: (v: "menu" | "ingresar" | "hparams") => void;
};

function Param({ label, value, onChange, remove }: { label: string; value: number | undefined; onChange: (v: number) => void; remove: () => void }) {
  return (
    <div className={`panel ${value === undefined ? "panelDisabled" : ""}`}>
      <label className="paramLabel">
        {label}
        <button className="btnClear" onClick={remove}>
          X
        </button>
      </label>
      <input
        className="input"
        type="number"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

export default function Hyperparametros({ setVista }: Props) {
  const [hp, setHp] = useState<HParams>({ 
    random_state: 42,
    learning_rate: 0.05,
    n_estimators: 2000,
    num_leaves: 40,
    feature_fraction: 0.8,
    lambda_l1: 0.1,
    lambda_l2: 0.1
  });

  const setVal = <K extends keyof HParams>(k: K, v: HParams[K]) => {
    setHp((prev) => ({ ...prev, [k]: v }));
  }

  const deleteVal = <K extends keyof HParams>(k: K) => {
    setHp((prev) => { 
      const copy = { ...prev };
      delete copy[k];
      return copy;
    });
  }


  const guardar = async () => {
    const API_BASE = "http://localhost:8000/api";

    try {
      const res = await fetch(`${API_BASE}/model`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(hp), 
      });

      if (!res.ok) {
        throw new Error(`Error saving hyperparameters: ${res.statusText}`);
      }

      alert("Hiperparámetros guardados exitosamente.");
    } catch (e) {
      alert("Error al guardar los hiperparámetros.");
      console.error(e);
    }
  };

  return (
    <section className="sectionParams">
      <div className="headerParams">
        <div>
          <div className="kicker">Settings</div>
          <h2>Tune your model</h2>
        </div>
      </div>
      <div className="formParams">
        <Param
          label="Random State"
          value={hp.random_state}
          onChange={(v) => setVal("random_state", v)}
          remove={() => deleteVal("random_state")}
        />
        <Param 
          label="Learning Rate"
          value={hp.learning_rate}
          onChange={(v) => setVal("learning_rate", v)}
          remove={() => deleteVal("learning_rate")}
        />  
        <Param
          label="Num Leaves"
          value={hp.num_leaves}
          onChange={(v) => setVal("num_leaves", v)}
          remove={() => deleteVal("num_leaves")}
        />
        <Param
          label="Nº Estimators"
          value={hp.n_estimators}
          onChange={(v) => setVal("n_estimators", v)}
          remove={() => deleteVal("n_estimators")}
        />
        <Param
          label="Feature Fraction"
          value={hp.feature_fraction}
          onChange={(v) => setVal("feature_fraction", v)}
          remove={() => deleteVal("feature_fraction")}
        />
         <Param
          label="Lambda L1"
          value={hp.lambda_l1}
          onChange={(v) => setVal("lambda_l1", v)}
          remove={() => deleteVal("lambda_l1")}
        />
         <Param
          label="Lambda L2"
          value={hp.lambda_l2}
          onChange={(v) => setVal("lambda_l2", v)}
          remove={() => deleteVal("lambda_l2")}
        />
      </div>
      <div className="actions">
        <button className="btn primary" onClick={guardar}>
          Guardar
        </button>
      </div>
      <div className="previewWrap">
        <h4 className="kicker">Preview</h4>
        <pre className="preview">{JSON.stringify(hp, null, 2)}</pre>
      </div>
    </section>
  );
}
