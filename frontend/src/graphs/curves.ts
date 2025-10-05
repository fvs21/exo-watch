type LightCurveParams = {
    periodDays: number;
    duration: number;
    depthPPM: number;
    impact: number;
    points?: number;
    nPeriods?: number;
};

function generateLightCurves({
    periodDays,
    duration,
    depthPPM,
    impact,
    points = 1000,
    nPeriods = 1
}: LightCurveParams) {
    const depthFrac = depthPPM / 1e6;
    const D = duration / 24;
    const rampFrac = Math.min(0.4, 0.1 + 0.3 * impact);
    const ramp = 0.5 * D * rampFrac;
    const flat = Math.max(D - 2 * ramp, 0);
    
    const totalSpan = periodDays * nPeriods;
    const phase = Array.from({ length: points  * nPeriods }, (_, i) => (i / (points * nPeriods)) * totalSpan - totalSpan / 2);

    const flux = phase.map((p) => {
        const x = Math.abs(p);
        if (x <= flat / 2) return 1 - depthFrac;     

        if (x <= flat / 2 + ramp) {                              
            const frac = (x - flat / 2) / ramp;
            return 1 - depthFrac * (1 - frac);
        }
        return 1;
    });

    return { phase, flux };
}

type SigmaFromSNRParams = {
    depthPPM: number;
    snr: number;
    durationHours: number;
    periodDays: number;
    cadenceMinutes?: number;
    obsDays?: number;
}

function sigmaFromSNR({
    depthPPM,
    snr,
    durationHours,
    periodDays,
    cadenceMinutes = 30,
    obsDays = 1320
}: SigmaFromSNRParams) {
    const depthFrac = depthPPM / 1e6;
    const ninPerTransit = Math.max(1, Math.floor((durationHours * 60) / cadenceMinutes));
    const nTransits = Math.max(1, Math.floor(obsDays / periodDays));
    const N_in = ninPerTransit * nTransits;                   // total in-transit points
    const sigma = depthFrac * (Math.sqrt(N_in) / Math.max(snr, 1e-6));
    return { sigma, ninPerTransit, nTransits, N_in };
}

function addGaussianNoise(arr: number[], sigma: number) {
    const randn = () => {
        let u = 0, v = 0;

        while (u == 0) u = Math.random();
        while (v == 0) v = Math.random();

        return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    }

    return arr.map(x => x + randn() * sigma);
}

export {
    generateLightCurves,
    sigmaFromSNR,
    addGaussianNoise
}