export type ModelType = "light_gbm" | "xgboost" | "random_forest";

export interface ParamConfig {
  key: string;
  label: string;
  defaultValue?: number | string;
  type: "number" | "string";
}

export interface ModelConfig {
  type: ModelType;
  name: string;
  params: ParamConfig[];
}

// LightGBM Configuration
export const lightGBMConfig: ModelConfig = {
  type: "light_gbm",
  name: "LightGBM",
  params: [
    { key: "random_state", label: "Random State", defaultValue: 42, type: "number" },
    { key: "learning_rate", label: "Learning Rate", defaultValue: 0.05, type: "number" },
    { key: "n_estimators", label: "Nº Estimators", defaultValue: 2000, type: "number" },
    { key: "num_leaves", label: "Num Leaves", defaultValue: 40, type: "number" },
    { key: "max_depth", label: "Max Depth", defaultValue: -1, type: "number" },
    { key: "feature_fraction", label: "Feature Fraction", defaultValue: 0.8, type: "number" },
    { key: "lambda_l1", label: "Lambda L1", defaultValue: 0.1, type: "number" },
    { key: "lambda_l2", label: "Lambda L2", defaultValue: 0.1, type: "number" },
  ],
};

// XGBoost Configuration
export const xgboostConfig: ModelConfig = {
  type: "xgboost",
  name: "XGBoost",
  params: [
    { key: "random_state", label: "Random State", defaultValue: 42, type: "number" },
    { key: "learning_rate", label: "Learning Rate", defaultValue: 0.02, type: "number" },
    { key: "n_estimators", label: "Nº Estimators", defaultValue: 1000, type: "number" },
    { key: "max_depth", label: "Max Depth", defaultValue: 8, type: "number" },
    { key: "subsample", label: "Subsample", defaultValue: 0.8, type: "number" },
    { key: "colsample_bytree", label: "Colsample Bytree", defaultValue: 0.8, type: "number" },
    { key: "reg_lambda", label: "Reg Lambda", defaultValue: 1.0, type: "number" },
    { key: "reg_alpha", label: "Reg Alpha", defaultValue: 0.1, type: "number" },
  ],
};

// Random Forest Configuration
export const randomForestConfig: ModelConfig = {
  type: "random_forest",
  name: "Random Forest",
  params: [
    { key: "random_state", label: "Random State", defaultValue: 42, type: "number" },
    { key: "n_estimators", label: "Nº Estimators", defaultValue: 300, type: "number" },
    { key: "max_depth", label: "Max Depth", defaultValue: 15, type: "number" },
    { key: "min_samples_leaf", label: "Min Samples Leaf", defaultValue: 5, type: "number" },
    { key: "min_samples_split", label: "Min Samples Split", defaultValue: 2, type: "number" },
  ],
};

// Model configurations map
export const modelConfigs: Record<ModelType, ModelConfig> = {
  light_gbm: lightGBMConfig,
  xgboost: xgboostConfig,
  random_forest: randomForestConfig,
};

// Helper to get default params for a model type
export const getDefaultParams = (modelType: ModelType): Record<string, any> => {
  const config = modelConfigs[modelType];
  const params: Record<string, any> = { model_type: modelType };
  
  config.params.forEach((param) => {
    if (param.defaultValue !== undefined) {
      params[param.key] = param.defaultValue;
    }
  });
  
  return params;
};
