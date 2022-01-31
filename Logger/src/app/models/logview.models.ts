export class Dashboard {
    public goodlogs: Array<GoodsLogs>
    public anomalyreference: Array<AnomalyReference>
  constructor() {
  }
}

export class GoodsLogs{
    frequency: number
    hash: string
    id: number
    last_occured: string
    name: string
    pattern: string
    plaintext: string
    constructor(

    ) { }
}

export class AnomalyReference{
    id: number
    last_occured: string
    name: string
    pattern: string
    plaintext: string
    resolution_steps: string
    root_cause: string
    hash: string
    constructor(

    ) { }
}