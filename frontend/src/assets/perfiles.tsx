type Campo = {
  key: string;
  label: string;
  min?: number;
  max?: number;
  decimals?: number;
};

export const PERFILES: Record<string, Campo[]> = {
  "Modelo (TESS)": [
    {
      key: "period",
      label: "Periodo (días)",
      min: 0.2,
      max: 50,
      decimals: 3,
    },
    {
      key: "depth",
      label: "Profundidad (ppm)",
      min: 50,
      max: 3000,
      decimals: 0,
    },
    {
      key: "duration",
      label: "Duración (hrs)",
      min: 0.5,
      max: 12,
      decimals: 2,
    },
    { key: "snr", label: "SNR", min: 1, max: 50, decimals: 2 },
    { key: "mag", label: "Magnitud", min: 6, max: 16, decimals: 2 },
    { key: "teff", label: "T_eff (K)", min: 3000, max: 7500, decimals: 0 },
  ],
  "Modelo (Kepler)": [
    {
      key: "period",
      label: "Periodo (días)",
      min: 0.2,
      max: 400,
      decimals: 3,
    },
    {
      key: "depth",
      label: "Profundidad (ppm)",
      min: 20,
      max: 20000,
      decimals: 0,
    },
    {
      key: "duration",
      label: "Duración (hrs)",
      min: 0.5,
      max: 20,
      decimals: 2,
    },
    { key: "snr", label: "SNR", min: 1, max: 200, decimals: 2 },
    {
      key: "rstar",
      label: "Radio estrella (R☉)",
      min: 0.3,
      max: 3,
      decimals: 3,
    },
    { key: "teff", label: "T_eff (K)", min: 3000, max: 9000, decimals: 0 },
  ],
  "Libre (6 campos)": [
    { key: "f1", label: "Dato 1" },
    { key: "f2", label: "Dato 2" },
    { key: "f3", label: "Dato 3" },
    { key: "f4", label: "Dato 4" },
    { key: "f5", label: "Dato 5" },
    { key: "f6", label: "Dato 6" },
  ],
};
