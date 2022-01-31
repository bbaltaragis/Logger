import { AnomalyReference } from "./logview.models"

export class Anomaly{
    public historicalAnomalies: Array<HistoricalAnomaly>
    public anomalyComments: Array<AnomalyComment>
    public anomalyReference: Array<AnomalyReference>
}

export class HistoricalAnomaly{
    public id: number
    public anomaly_id: number
    public plaintext: string
    public date_occured: string
}

export class AnomalyComment{
    public id: number
    public anomaly_id: number
    public comment: string
    public username: string
}