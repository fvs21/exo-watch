#!/bin/bash

echo "======================================================"
echo "Database Schema Verification"
echo "======================================================"

DB_PATH="./backend/app/db.sqlite3"

if [ ! -f "$DB_PATH" ]; then
    echo "❌ Database not found at $DB_PATH"
    exit 1
fi

echo "✅ Database file found"
echo ""

echo "Tables in database:"
echo "------------------------------------------------------"
sqlite3 "$DB_PATH" "SELECT name FROM sqlite_master WHERE type='table';"
echo ""

echo "Model table schema:"
echo "------------------------------------------------------"
sqlite3 "$DB_PATH" ".schema model"
echo ""

echo "LightGBM params table schema:"
echo "------------------------------------------------------"
sqlite3 "$DB_PATH" ".schema lightgbm_params"
echo ""

echo "XGBoost params table schema:"
echo "------------------------------------------------------"
sqlite3 "$DB_PATH" ".schema xgboost_params"
echo ""

echo "Random Forest params table schema:"
echo "------------------------------------------------------"
sqlite3 "$DB_PATH" ".schema randomforest_params"
echo ""

echo "Record counts:"
echo "------------------------------------------------------"
echo -n "Models: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM model;"
echo -n "LightGBM params: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM lightgbm_params;"
echo -n "XGBoost params: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM xgboost_params;"
echo -n "Random Forest params: "
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM randomforest_params;"
echo ""

echo "Sample data from model table:"
echo "------------------------------------------------------"
sqlite3 "$DB_PATH" -header -column "SELECT id, name, model_type, accuracy, roc_auc FROM model LIMIT 5;"

echo ""
echo "✅ Schema verification complete"
