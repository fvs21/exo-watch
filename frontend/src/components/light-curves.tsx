import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function LightCurves({ period, duration, depth, snr, impact }) {
  // Simular una curva de luz idealizada
  const points = 200;
  const data = Array.from({ length: points }, (_, i) => {
    const phase = (i / points) * period;
    // Generar una caída durante el tránsito
    const brightness =
      phase % period > duration / 2 && phase % period < period - duration / 2
        ? 1
        : 1 - depth;
    return { phase, brightness };
  });

  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-2">Curva de luz simulada</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="phase" label={{ value: "Fase orbital", position: "insideBottom", offset: -5 }} />
          <YAxis domain={[1 - depth * 2, 1]} label={{ value: "Brillo normalizado", angle: -90, position: "insideLeft" }} />
          <Tooltip />
          <Line type="monotone" dataKey="brightness" stroke="#8884d8" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
