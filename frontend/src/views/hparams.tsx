import { useState } from "react";
import "../styles/app.css";
import "../styles/hparams.css";

type HParams = {
  learningRate: number;
  epochs: number;
  batchSize: number;
  optimizer: "adam" | "sgd" | "rmsprop" | "adamw";
  weightDecay: number; // L2
  dropout: number; // 0..1
  seed: number;
  datasetName?: string;
};

type Props = {
  setVista: (v: "menu" | "ingresar" | "hparams") => void;
};

export default function Hyperparametros({ setVista }: Props) {
  const [hp, setHp] = useState<HParams>({
    learningRate: 0.001,
    epochs: 20,
    batchSize: 32,
    optimizer: "adam",
    weightDecay: 0.0,
    dropout: 0.0,
    seed: 42,
    datasetName: undefined,
  });

  const setVal = <K extends keyof HParams>(k: K, v: HParams[K]) =>
    setHp((prev) => ({ ...prev, [k]: v }));

  const handleDataset = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setVal("datasetName", file.name);
    alert(`Dataset seleccionado: ${file.name}`);
  };

  const guardar = () => {
    console.log("Hiperparámetros guardados:", hp);
    alert("Hiperparámetros listos (revisa la consola).");
  };

  return (
    <section className="sectionParams">
      <div className="headerParams">
        <div>
          <div className="kicker">Configuración</div>
          <h2>Configura los Hiperparámetros de tu modelo</h2>
        </div>
        <div className="badge">
          ⚙️ Optimizer:{" "}
          <strong style={{ marginLeft: 6 }}>{hp.optimizer}</strong>
        </div>
      </div>

      <div className="formParams">
        <div className="panel">
          <label className="label">Learning Rate</label>
          <input
            className="input"
            type="number"
            step="0.0001"
            min={0}
            value={hp.learningRate}
            onChange={(e) => setVal("learningRate", Number(e.target.value))}
          />
        </div>

        <div className="panel">
          <label className="label">Epochs</label>
          <input
            className="input"
            type="number"
            min={1}
            value={hp.epochs}
            onChange={(e) => setVal("epochs", Number(e.target.value))}
          />
        </div>

        <div className="panel">
          <label className="label">Batch Size</label>
          <input
            className="input"
            type="number"
            min={1}
            value={hp.batchSize}
            onChange={(e) => setVal("batchSize", Number(e.target.value))}
          />
        </div>

        <div className="panel">
          <label className="label">Optimizer</label>
          <select
            className="input"
            value={hp.optimizer}
            onChange={(e) =>
              setVal("optimizer", e.target.value as HParams["optimizer"])
            }
          >
            <option value="adam">Adam</option>
            <option value="adamw">AdamW</option>
            <option value="sgd">SGD</option>
            <option value="rmsprop">RMSProp</option>
          </select>
        </div>

        <div className="panel">
          <label className="label">Weight Decay (L2)</label>
          <input
            className="input"
            type="number"
            step="0.0001"
            min={0}
            value={hp.weightDecay}
            onChange={(e) => setVal("weightDecay", Number(e.target.value))}
          />
        </div>

        <div className="panel">
          <label className="label">Dropout (0 a 1)</label>
          <input
            className="input"
            type="number"
            step="0.01"
            min={0}
            max={1}
            value={hp.dropout}
            onChange={(e) => setVal("dropout", Number(e.target.value))}
          />
        </div>

        <div className="panel">
          <label className="label">Seed</label>
          <input
            className="input"
            type="number"
            min={0}
            value={hp.seed}
            onChange={(e) => setVal("seed", Number(e.target.value))}
          />
        </div>

        <div className="panel">
          <label className="label">Añadir dataset (entrenamiento)</label>
          <input
            className="file"
            type="file"
            accept=".csv,.parquet,.jsonl,.json"
            onChange={handleDataset}
          />
          {hp.datasetName && (
            <small className="muted">Seleccionado: {hp.datasetName}</small>
          )}
        </div>
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
