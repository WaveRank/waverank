import InputBox from "../components/InputBox";
import "../src/App.css";


export default function HomePage() {
    return (
        <div>
            <div className="body">

                <div className="bodyLeft">
                    <InputBox/>
                    <div className="analysisBox">
                        <h2>Analysis</h2>
                        <p>Status: ???</p>
                        <p>Bar chart here</p>
                    </div>
                </div>

                <div className="bodyRight">
                    <div className="dataBox">
                        <h2>Data</h2>
                        <p>Graphs here</p>
                    </div>
                </div>

            </div>
        </div>
    );
};