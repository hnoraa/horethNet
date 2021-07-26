import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private url = "http://localhost:5000";
  constructor(private server: HttpClient) { }

  public test() {
    console.log('in test');
    return this.server.get(`${this.url}/test`);
  }
}
