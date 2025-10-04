import { useMemo, useState } from "react";
import Dropdown from "../components/dropdown";
import { PERFILES } from "../assets/perfiles";
import "../styles/app.css";
import "../styles/ingresarDatos.css";

type Props = {
  setVista: (v: "menu" | "ingresar" | "hparams") => void;
};

type Campo = {
  key: string;
  label: string;
  min?: number;
  max?: number;
  decimals?: number;
};

type ModeloResponse = {
  ok: boolean;
  prediction?: string | number | boolean;
  score?: number;
  details?: unknown;
  error?: string;
};

export default function IngresarDatos({ setVista }: Props) {
  const [modelo, setModelo] = useState<number | null>(null);
  const campos = useMemo<Campo[]>(
    () => PERFILES[modelo ?? 0] as Campo[],
    [modelo]
  );

  const [data, setData] = useState<Record<string, number | null>>({});

  const [payloadPreview, setPayloadPreview] = useState<boolean>(false);
  const [respuesta, setRespuesta] = useState<ModeloResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const changeData = (key: string, value: string) => {
    if (isNaN(Number(value))) return;
    else if (value === "") setData((prev) => ({ ...(prev ?? {}), [key]: null }));
    else setData((prev) => ({ ...(prev ?? {}), [key]: Number(value) }));
  };

  const generarAleatorios = () => {
    const next = campos.map((c) => {
      if (c.min === undefined || c.max === undefined) {
        return (Math.random() * 100).toFixed(c.decimals ?? 2);
      }
      const val = c.min + Math.random() * (c.max - c.min);
      return (c.decimals ?? 2) === 0
        ? Math.round(val)
        : val.toFixed(c.decimals ?? 2);
    });
    setData(() => {
      const obj: Record<string, number> = {};
      campos.forEach((c, i) => {
        obj[c.key] = Number(next[i]);
      });
      return obj;
    });
  };

  const handleCSV = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) alert(`CSV selected: ${file.name}`);
  };

  const enviar = async () => {
    setPayloadPreview(true);
    setRespuesta(null);
    setErrorMsg(null);
    setLoading(true);

    const API_BASE = "http://localhost:8000/api"; // Cambia esto si tu backend está en otra URL
    try {
      // 🔁 Cambia esta URL por tu endpoint real
      const res = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: modelo,
          features: data,
        }),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `HTTP ${res.status}`);
      }

      const resData: ModeloResponse = await res.json();
      setRespuesta(resData);
    } catch (err: any) {
      setErrorMsg(err?.message ?? "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const onChangeModelo = (m: number) => setModelo(m);

  return (
    <section className="sectionData">
      <div className="container">
        <div>Input</div>
        <div className="header">
          <div className="kicker">
            <h2>Enter Data</h2>
            <h2>Select a model</h2>
          </div>
        </div>

        <div className="dataRow">
          <div className="panel">
            <label className="labelData">Upload CSV</label>

            <input
              id="csvInput"
              type="file"
              accept=".csv"
              onChange={handleCSV}
              style={{ display: "none" }}
            />
            <label htmlFor="csvInput" className="fileSelector">
              Select file
            </label>
          </div>

          <div className="panel">
            <label className="labelData">
              <strong>Model</strong>
            </label>
            <Dropdown
              options={["Base"]}
              value={modelo}
              onChange={onChangeModelo}
              onAdd={() => setVista("hparams")}
            />
          </div>
        </div>
        <div>
          <p className="infoText">You can enter data manually</p>
          <div className="inputsGrid section">
            {campos.map((campo, i) => (
              <div key={campo.key} className="card">
                <label className="labelData" htmlFor={`campo-${i}`}>
                  {campo.label}
                </label>
                <input
                  className="input"
                  id={`campo-${i}`}
                  type="number"
                  placeholder={campo.label}
                  value={data[campo.key as keyof typeof data] ?? ""}
                  onChange={(e) => changeData(campo.key, e.target.value)}
                />
              </div>
            ))}
          </div>
        </div>

        <div className="actions">
          <button className="btn" onClick={generarAleatorios}>
            🎲 Generate random
          </button>
          <button className="btn primary" onClick={enviar} disabled={loading}>
            {loading ? "Sending..." : "Send to model"}
          </button>
        </div>
        {/* 🔎 PREVIEW de lo enviado y lo recibido */}
        <div className="previewWrap">
          <div className="previewBlock">
            <h4 className="kicker">Payload</h4>
            <pre className="preview">
              {payloadPreview
                ? JSON.stringify(data, null, 2)
                : "// Press 'Send to model' to see the payload"}
            </pre>
          </div>
          <div className="previewBlock">
            <h4 className="kicker">Model response</h4>
            {errorMsg ? (
              <div className="alert error">⚠️ {errorMsg}</div>
            ) : (
              <pre className="preview">
                {respuesta
                  ? JSON.stringify(respuesta, null, 2)
                  : "// No response yet"}
              </pre>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
