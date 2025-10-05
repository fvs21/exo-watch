import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "app", "db.sqlite3")

def migrate_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    # Create new tables for each model type
    print("Creating lightgbm_params table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lightgbm_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learning_rate REAL,
            n_estimators INTEGER,
            num_leaves INTEGER,
            max_depth INTEGER,
            lambda_l1 REAL,
            lambda_l2 REAL,
            feature_fraction REAL,
            random_state INTEGER
        )
    """)
    
    print("Creating xgboost_params table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xgboost_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learning_rate REAL,
            n_estimators INTEGER,
            max_depth INTEGER,
            subsample REAL,
            colsample_bytree REAL,
            reg_lambda REAL,
            reg_alpha REAL,
            objective TEXT,
            eval_metric TEXT,
            random_state INTEGER
        )
    """)
    
    print("Creating randomforest_params table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS randomforest_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            n_estimators INTEGER,
            max_depth INTEGER,
            min_samples_leaf INTEGER,
            min_samples_split INTEGER,
            random_state INTEGER
        )
    """)
    
    # Create new model table
    print("Creating new model_new table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            model_type TEXT NOT NULL,
            accuracy REAL,
            roc_auc REAL,
            pr_auc REAL,
            lightgbm_params_id INTEGER,
            xgboost_params_id INTEGER,
            randomforest_params_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lightgbm_params_id) REFERENCES lightgbm_params(id),
            FOREIGN KEY (xgboost_params_id) REFERENCES xgboost_params(id),
            FOREIGN KEY (randomforest_params_id) REFERENCES randomforest_params(id)
        )
    """)
    
    # Migrate existing data
    print("Migrating existing data...")
    cursor.execute("SELECT * FROM model_new")
    rows = cursor.fetchall()
    
    for row in rows:
        # Get column names
        cursor.execute("PRAGMA table_info(model_new)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Create a dict from row data
        data = dict(zip(columns, row))
        
        model_type = data.get('model_type', 'light_gbm')
        params_id = None
        
        if model_type == 'light_gbm':
            cursor.execute("""
                INSERT INTO lightgbm_params (
                    learning_rate, n_estimators, num_leaves, max_depth,
                    lambda_l1, lambda_l2, feature_fraction, random_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('learning_rate'),
                data.get('n_estimators'),
                data.get('num_leaves'),
                data.get('max_depth'),
                data.get('lambda_l1'),
                data.get('lambda_l2'),
                data.get('feature_fraction'),
                data.get('random_state')
            ))
            params_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO model_new (
                    name, path, model_type, accuracy, roc_auc, pr_auc, lightgbm_params_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('name'),
                data.get('path'),
                model_type,
                data.get('accuracy'),
                data.get('roc_auc'),
                data.get('pr_auc'),
                params_id
            ))
            
        elif model_type == 'xgboost':
            cursor.execute("""
                INSERT INTO xgboost_params (
                    learning_rate, n_estimators, max_depth, subsample,
                    colsample_bytree, reg_lambda, reg_alpha, objective, 
                    eval_metric, random_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('learning_rate'),
                data.get('n_estimators'),
                data.get('max_depth'),
                data.get('subsample'),
                data.get('colsample_bytree'),
                data.get('reg_lambda'),
                data.get('reg_alpha'),
                data.get('objective'),
                data.get('eval_metric'),
                data.get('random_state')
            ))
            params_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO model_new (
                    name, path, model_type, accuracy, roc_auc, pr_auc, xgboost_params_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('name'),
                data.get('path'),
                model_type,
                data.get('accuracy'),
                data.get('roc_auc'),
                data.get('pr_auc'),
                params_id
            ))
            
        elif model_type == 'random_forest':
            cursor.execute("""
                INSERT INTO randomforest_params (
                    n_estimators, max_depth, min_samples_leaf, 
                    min_samples_split, random_state
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                data.get('n_estimators'),
                data.get('max_depth'),
                data.get('min_samples_leaf'),
                data.get('min_samples_split'),
                data.get('random_state')
            ))
            params_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO model_new (
                    name, path, model_type, accuracy, roc_auc, pr_auc, randomforest_params_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('name'),
                data.get('path'),
                model_type,
                data.get('accuracy'),
                data.get('roc_auc'),
                data.get('pr_auc'),
                params_id
            ))
    
    # Drop old table and rename new one
    print("Replacing old model table...")
    cursor.execute("DROP TABLE IF EXISTS model")
    cursor.execute("ALTER TABLE model_new RENAME TO model")
    
    conn.commit()
    conn.close()
    
    print("Migration complete!")

if __name__ == '__main__':
    migrate_database()
