
import { sigmaFromSNR, addGaussianNoise, generateLightCurves } from "../graphs/curves";
import Plot from "react-plotly.js";

type Props = {
    period: number;
    duration: number;
    depth: number;
    snr: number;
    impact: number;
}

export default function LightCurves({ period, duration, depth, snr, impact }: Props) {
    const { phase, flux } = generateLightCurves({ periodDays: period, duration, depthPPM: depth, impact, nPeriods: 1 });

    const { sigma } = sigmaFromSNR({ depthPPM: depth, snr, durationHours: duration, periodDays: period });
    const fluxWithNoise = addGaussianNoise(flux, sigma);

    return (
        <Plot
            data={[
                {
                    x: phase,
                    y: fluxWithNoise,
                    type: "scatter",
                    mode: "lines",
                    name: "Signal + Noise",
                },
            ]}
            layout={{
                title: { text: "Light Curve" }
            }}
        />
    );
}