import React from "react";
import "../styles/dinamicTables.css"; // Importamos el archivo CSS actualizado

interface DynamicTableProps {
  data: Record<string, any>[];
}

const DynamicTable: React.FC<DynamicTableProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <p className="no-data-message">No data to show.</p>;
  }

  // Obtener las claves (columnas) desde el primer objeto
  const headers = Object.keys(data[0]);

  return (
    <div className="table-container">
      <table className="dynamic-table">
        <thead>
          <tr>
            {/* Columna para la enumeración */}
            <th>#</th> 
            {headers.map((header) => (
              <th key={header}>
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              {/* Celda con el número de fila (índice + 1) */}
              <td>{i + 1}</td>
              {headers.map((header) => (
                <td key={header}>
                  {row[header] ?? "N/A"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DynamicTable;