import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'hackaton-speech2text-glossary-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeaderComponent {}
