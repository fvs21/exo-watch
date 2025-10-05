import { memo } from "react";
import { sigmaFromSNR, addGaussianNoise, generateLightCurves } from "../graphs/curves";
import Plot from "react-plotly.js";

type Props = {
    period: number;
    duration: number;
    depth: number;
    snr: number;
    impact: number;
}

function LightCurves({ period, duration, depth, snr, impact }: Props) {
    const { x, flux } = generateLightCurves({ periodDays: period, durationHours: duration, depthPPM: depth, impact, nPeriods: 1, t0BKJD: 100, returnPhaseUnits: true });

    const { sigma } = sigmaFromSNR({ depthPPM: depth, snr, durationHours: duration, periodDays: period });
    const fluxWithNoise = addGaussianNoise(flux, sigma);

    return (
        <Plot
            data={[
                {
                    x: x,
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

export default memo(LightCurves);
