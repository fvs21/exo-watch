// DynamicTable.tsx
import "../styles/dinamicTables.css";

const DynamicTable = ({ data }: { data: Record<string, any>[] }) => {
  if (!data || data.length === 0) return <p>No hay datos para mostrar.</p>;

  const headers = Object.keys(data[0]);

  return (
    <div className="dynamic-table-container">
      <table className="dynamic-table">
        <thead>
          <tr> 
            {headers.map((h) => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              {headers.map((h) => (
                <td key={h}>
                  {row[h] === null || row[h] === undefined || isNaN(row[h])
                    ? "N/A"
                    : row[h]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// EXPORT por defecto
export default DynamicTable;
