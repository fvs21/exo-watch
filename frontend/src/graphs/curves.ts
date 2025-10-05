type LightCurveParams = {
  periodDays: number;          
  durationHours: number;       
  depthPPM: number;           
  impact?: number;             
  points?: number;            
  nPeriods?: number;          
  t0BKJD?: number;            
  returnPhaseUnits?: boolean; 
};

type SigmaFromSNRParams = {
  depthPPM: number;
  snr: number;
  durationHours: number;
  periodDays: number;
  cadenceMinutes?: number;     
  obsDays?: number;            
  dutyCycle?: number;          
};

export function sigmaFromSNR({
  depthPPM,
  snr,
  durationHours,
  periodDays,
  cadenceMinutes = 30,
  obsDays = 1320,
  dutyCycle = 0.9,
}: SigmaFromSNRParams) {
  const depthFrac = Math.max(0, depthPPM) / 1e6;
  const ninPerTransit = Math.max(1, Math.floor((durationHours * 60) / cadenceMinutes));
  const nTransits = Math.max(1, Math.floor((obsDays * dutyCycle) / Math.max(periodDays, 1e-9)));
  const N_in = Math.max(1, ninPerTransit * nTransits);
  const sigma = depthFrac * (Math.sqrt(N_in) / Math.max(snr, 1e-9));
  return { sigma, ninPerTransit, nTransits, N_in };
}

export function addGaussianNoise(arr: number[], sigma: number, rng: () => number = Math.random) {
  const randn = () => {
    let u = 0, v = 0;
    while (u === 0) u = rng();
    while (v === 0) v = rng();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };
  return arr.map(x => x + randn() * sigma);
}

export function addRedNoise(arr: number[], amplitude: number, periodSamples: number) {
  if (amplitude <= 0 || !isFinite(periodSamples) || periodSamples <= 1) return arr.slice();
  return arr.map((v, i) => v + amplitude * Math.sin((2 * Math.PI * i) / periodSamples));
}

export function generateLightCurves({
  periodDays,
  durationHours,
  depthPPM,
  impact = 0.3,
  points = 1000,
  nPeriods = 1,
  t0BKJD = 0,
  returnPhaseUnits = false,
}: LightCurveParams) {
  const P = Math.max(periodDays, 1e-9);
  const D = Math.max(durationHours, 1e-9) / 24;      
  const d = Math.max(0, depthPPM) / 1e6;             
  const b = Math.min(Math.max(impact, 0), 1.1);
  const totalPoints = Math.max(2, Math.floor(points) * Math.max(1, Math.floor(nPeriods)));

  const rampFrac = Math.min(0.4, Math.max(0.1, 0.1 + 0.3 * b));
  const ramp = 0.5 * D * rampFrac;
  const flat = Math.max(D - 2 * ramp, 0);
  const eps = 1e-12;

  const span = P * Math.max(1, Math.floor(nPeriods));
  const tStart = t0BKJD - span / 2;
  const dt = span / (totalPoints - 1);
  const time = Array.from({ length: totalPoints }, (_, i) => tStart + i * dt);

  const flux = new Array<number>(totalPoints);
  for (let i = 0; i < totalPoints; i++) {
    const phi = ((time[i] - t0BKJD + 0.5 * P) % P) - 0.5 * P;
    const x = Math.abs(phi);

    if (x <= flat / 2) {
      flux[i] = 1 - d; 
    } else if (x <= flat / 2 + Math.max(ramp, eps)) {
      const frac = (x - flat / 2) / Math.max(ramp, eps);
      flux[i] = 1 - d * (1 - frac); 
    } else {
      flux[i] = 1;
    }
  }

  const xAxis = returnPhaseUnits
    ? time.map(t => ((t - t0BKJD) / P))     
    : time;                                

  return { x: xAxis, flux, meta: { P, D, depthFrac: d, impact: b, ramp, flat, t0BKJD } };
}