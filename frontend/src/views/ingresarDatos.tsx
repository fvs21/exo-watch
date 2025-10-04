import { useEffect, useMemo, useState } from "react";
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
  const [modelo, setModelo] = useState<string | null>("Libre (6 campos)");
  const campos = useMemo<Campo[]>(
    () => PERFILES[modelo ?? "Libre (6 campos)"] as Campo[],
    [modelo]
  );

  const [inputs, setInputs] = useState<string[]>([]);
  const [payloadPreview, setPayloadPreview] = useState<object | null>(null);
  const [respuesta, setRespuesta] = useState<ModeloResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    setInputs(Array.from({ length: campos.length }, (_, i) => inputs[i] ?? ""));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [campos]);

  const setAt = (i: number, value: string) => {
    setInputs((prev) => {
      const next = [...prev];
      next[i] = value;
      return next;
    });
  };

  const generarAleatorios = () => {
    const next = campos.map((c) => {
      if (c.min === undefined || c.max === undefined) {
        return (Math.random() * 100).toFixed(c.decimals ?? 2);
      }
      const val = c.min + Math.random() * (c.max - c.min);
      return (c.decimals ?? 2) === 0
        ? String(Math.round(val))
        : val.toFixed(c.decimals ?? 2);
    });
    setInputs(next);
  };

  const handleCSV = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) alert(`CSV seleccionado: ${file.name}`);
  };

  const enviar = async () => {
    const payload = Object.fromEntries(
      campos.map((c, i) => [c.key, inputs[i] ?? ""])
    );

    setPayloadPreview(payload);
    setRespuesta(null);
    setErrorMsg(null);
    setLoading(true);

    try {
      // 🔁 Cambia esta URL por tu endpoint real
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          modeloSeleccionado: modelo,
          datos: payload,
        }),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `HTTP ${res.status}`);
      }

      const data: ModeloResponse = await res.json();
      setRespuesta(data);
    } catch (err: any) {
      setErrorMsg(err?.message ?? "Error desconocido");
    } finally {
      setLoading(false);
    }
  };

  const onChangeModelo = (m: string) => setModelo(m);

  return (
    <section className="sectionData">
      <div className="container">
        <div>Entrada</div>
        <div className="header">
          <div className="kicker">
            <h2>Ingresar Datos</h2>
            <h2>Selecciona un modelo</h2>
          </div>
        </div>

        <div className="dataRow">
          <div className="panel">
            <label className="labelData">Cargar CSV</label>

            <input
              id="csvInput"
              type="file"
              accept=".csv"
              onChange={handleCSV}
              style={{ display: "none" }}
            />
            <label htmlFor="csvInput" className="fileSelector">
              Seleccionar archivo
            </label>
          </div>

          <div className="panel">
            <label className="labelData">
              <strong>Modelo</strong>
            </label>
            <Dropdown
              options={Object.keys(PERFILES)}
              value={modelo}
              onChange={onChangeModelo}
              onAdd={() => setVista("hparams")}
            />
          </div>
        </div>

        <div>
          <p className="infoText"> Puedes cargar los datos manualmente</p>

          <div className="inputsGrid section">
            {campos.map((campo, i) => (
              <div key={campo.key} className="card">
                <label className="labelData" htmlFor={`campo-${i}`}>
                  {campo.label}
                </label>
                <input
                  className="input"
                  id={`campo-${i}`}
                  type={
                    campo.min !== undefined && campo.max !== undefined
                      ? "number"
                      : "text"
                  }
                  step={
                    campo.decimals !== undefined
                      ? 1 / 10 ** campo.decimals
                      : undefined
                  }
                  min={campo.min}
                  max={campo.max}
                  inputMode={campo.min !== undefined ? "decimal" : undefined}
                  placeholder={campo.label}
                  value={inputs[i] ?? ""}
                  onChange={(e) => setAt(i, e.target.value)}
                />
              </div>
            ))}
          </div>
        </div>

        <div className="actions">
          <button className="btn" onClick={generarAleatorios}>
            🎲 Generar aleatorios
          </button>
          <button className="btn primary" onClick={enviar} disabled={loading}>
            {loading ? "Enviando..." : "Enviar a modelo"}
          </button>
        </div>

        {/* 🔎 PREVIEW de lo enviado y lo recibido */}
        <div className="previewWrap">
          <div className="previewBlock">
            <h4 className="kicker">Payload</h4>
            <pre className="preview">
              {payloadPreview
                ? JSON.stringify(payloadPreview, null, 2)
                : "// Presiona 'Enviar a modelo' para ver el payload"}
            </pre>
          </div>

          <div className="previewBlock">
            <h4 className="kicker">Respuesta del modelo</h4>
            {errorMsg ? (
              <div className="alert error">⚠️ {errorMsg}</div>
            ) : (
              <pre className="preview">
                {respuesta
                  ? JSON.stringify(respuesta, null, 2)
                  : "// Aún no hay respuesta"}
              </pre>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
