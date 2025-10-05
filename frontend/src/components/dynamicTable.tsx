import React from "react";

interface DynamicTableProps {
  data: Record<string, any>[];
}

const DynamicTable: React.FC<DynamicTableProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <p className="text-gray-500">No hay datos para mostrar.</p>;
  }

  // Obtener las claves (columnas) desde el primer objeto
  const headers = Object.keys(data[0]);

  return (
    <div className="p-4 overflow-x-auto">
      <table className="min-w-full border border-gray-300 rounded-lg shadow-sm">
        <thead className="bg-gray-100">
          <tr>
            {headers.map((header) => (
              <th
                key={header}
                className="border px-3 py-2 text-left font-semibold capitalize"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
              {headers.map((header) => (
                <td key={header} className="border px-3 py-2">
                  {row[header]}
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
