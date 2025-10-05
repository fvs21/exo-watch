import React from "react";
import "../styles/dinamicTables.css"; // Importamos el nuevo archivo CSS

interface DynamicTableProps {
  data: Record<string, any>[];
}

const DynamicTable: React.FC<DynamicTableProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <p className="no-data-message">No hay datos para mostrar.</p>;
  }

  // Obtener las claves (columnas) desde el primer objeto
  const headers = Object.keys(data[0]);

  return (
    <div className="table-container">
      <table className="dynamic-table">
        <thead>
          <tr>
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
              {headers.map((header) => (
                <td key={header}>
                  {/* Si el valor no existe o es nulo, muestra 'N/A' */}
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