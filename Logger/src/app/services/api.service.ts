import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { Dashboard } from '../models/logview.models';
import { Anomaly } from '../models/anomaly.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {


  private REST_API_SERVER = "http://localhost:8000/";
  constructor(private httpClient: HttpClient) { }

  getDashboard(url: string) : Observable<Dashboard>{
    return this.httpClient.get<Dashboard>(this.REST_API_SERVER + 'dashboard');
  }
  
  getAnomaly(url: string) : Observable<Anomaly>{
    return this.httpClient.get<Anomaly>(this.REST_API_SERVER + 'anomaly/' + url);
  }

  postComment(comment: string, id: string) {
    let payload = {
      "anomaly_id": id,
      "comment": comment,
      "username": "admin"
    }
    const header = new HttpHeaders()
    .set('Content-type', 'application/json');
    const body = JSON.stringify(payload);
    console.log(body);
    return this.httpClient.post<Anomaly>(this.REST_API_SERVER+'anomaly/' + id + '/comment', body, { headers: header });
  }

    patchResolutionSteps(resolution: string, id: string) {
    let payload = {
      "id": id,
      "resolution_steps": resolution
    }
    const header = new HttpHeaders()
    .set('Content-type', 'application/json');
    const body = JSON.stringify(payload);
    console.log(body);
    return this.httpClient.patch<String>(this.REST_API_SERVER+'anomaly/' + id + '/updateResolutionSteps', body, { headers: header });
  }

    patchRootCause(rootCause: string, id: string) {
    let payload = {
      "id": id,
      "root_cause": rootCause
    }
    const header = new HttpHeaders()
    .set('Content-type', 'application/json');
    const body = JSON.stringify(payload);
    console.log(body);
    return this.httpClient.patch<String>(this.REST_API_SERVER+'anomaly/' + id + '/updateRootCause', body, { headers: header });
  }

}