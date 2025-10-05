import { useState } from "react";
import "../styles/app.css";
import "../styles/hparams.css";
import { 
  type ModelType, 
  modelConfigs, 
  getDefaultParams
} from "../config/modelConfigs";
import DynamicTable from "../components/dynamicTable";

type Props = {
  setVista: (v: "menu" | "ingresar" | "hparams") => void;
};

function Param({ 
  label, 
  value, 
  onChange, 
  remove,
  type = "number"
}: { 
  label: string; 
  value: number | string | undefined; 
  onChange: (v: number | string) => void; 
  remove: () => void;
  type?: "number" | "string";
}) {
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
        type={type === "number" ? "number" : "text"}
        value={value}
        onChange={(e) => onChange(type === "number" ? Number(e.target.value) : e.target.value)}
      />
    </div>
  );
}

export default function Hyperparametros({ setVista }: Props) {
  const [modelType, setModelType] = useState<ModelType>("light_gbm");
  const [hp, setHp] = useState<Record<string, any>>(getDefaultParams("light_gbm"));

  const setVal = (k: string, v: any) => {
    setHp((prev) => ({ ...prev, [k]: v }));
  }

  const deleteVal = (k: string) => {
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

      alert("Hyperparameters saved successfully.");
    } catch (e) {
      alert("Error saving hyperparams.");
      console.error(e);
    }
  };

  const handleModelTypeChange = (newType: ModelType) => {
    setModelType(newType);
    setHp(getDefaultParams(newType));
  };

  const currentConfig = modelConfigs[modelType];

  return (
    <section className="sectionParams">
      <div className="headerParams">
        <div>
          <div className="kicker">Settings</div>
          <h2>Tune your model</h2>
        </div>
      </div>
      
      <div className="formParams">
        <div className="panel">
          <label className="paramLabel">Model Type</label>
          <select 
            className="input" 
            value={modelType} 
            onChange={(e) => handleModelTypeChange(e.target.value as ModelType)}
          >
            <option value="light_gbm">LightGBM</option>
            <option value="xgboost">XGBoost</option>
            <option value="random_forest">Random Forest</option>
          </select>
        </div>

        {/* Render parameters dynamically based on config */}
        {currentConfig.params.map((paramConfig) => (
          <Param
            key={paramConfig.key}
            label={paramConfig.label}
            value={hp[paramConfig.key]}
            onChange={(v) => setVal(paramConfig.key, v)}
            remove={() => deleteVal(paramConfig.key)}
            type={paramConfig.type}
          />
        ))}
        
      </div>

      <div className="actions">
        <button className="btn primary" onClick={guardar}>
          Save
        </button>
      </div>
      <div className="previewWrap">
        <h4 className="kicker">Preview</h4>
        <DynamicTable
    data={currentConfig.params.map((paramConfig) => ({
      "Parameter": paramConfig.label,
      "Value": hp[paramConfig.key] ?? "Not established",
    }))}
  />
) : (
  <p>No hay parámetros para mostrar.</p>
      </div>
    </section>
  );
}
